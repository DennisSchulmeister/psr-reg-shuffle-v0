#encoding=utf-8

# bankfile.py
# This file is part of PSR Registration Shuffler
#
# Copyright (C) 2008 - Dennis Schulmeister  <dennis -at- ncc-1701a.homelinux.net>
#
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# It is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this file. If not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor,
# Boston, MA  02110-1301  USA

'''
PURPOSE
=======

All classes dealing with bank files are supposed to inherit from the base class
in order to stick to a common API. The following operations are covered by the
API:

* Check if a given file can be used with a given class
* Open existing bank file
* Create a new bank file in memory
* Extract registrations
* Import registrations
* Store bank file on disk

Operations in the registrations itself are not covered here. That's what the
package registration is for. So this package merely resembles access to bank
files as a container for registrations. The package regfile works the same
by acting as a container accessor for files which hold registration objects.
'''

# Public export of module content
__all__ = [
    "BankFile"
]


# Import applicaiton modules
from .. import classfinder
from .. import util

from ..appexceptions import NoClassFound
from ..appexceptions import NoFileGiven

import appexceptions
import registration
import modelspecific


# Define BankFile meta-class
class MetaBankFile(modelspecific.MetaModelSpecific):
    '''
    Meta-class for class Registration.
    '''

    def __init__(cls, name, bases, dict):
        '''
        Constructor. Called after class definition of class BankFile.
        Injects class attributes "classFinderByName" and "classFinderByFile"
        for looking up suitable sub-classes by keyboard name and bank file.
        '''
        # Initialize class as usual
        super(MetaBankFile, cls).__init__(name, bases, dict)

        # Inject classFinder class attributes
        classFinderByFile = classfinder.ClassFinder(
            superClass   = cls,
            classes      = __RB_CLASSES__,
            testMethName = "canUnderstandFile",
            hashMethName = "hashFile"
        )
        setattr(cls, 'classFinderByFile', classFinderByFile)


# Define BankFile class
class BankFile(modelspecific.ModelSpecific):
    '''
    This is the base class which defines a common API for all classes dealing
    with bank files.
    '''

    # Meta-class for injecting ClassFinder objects as class attribute.
    # NOTE: You cannot access the class object during definition of a class.
    # However the ClassFinders need a super-class as an upper search limit so
    # a meta-class must be used in order to provide that information.
    __metaclass__ = MetaBankFile

    # User-information shown on the keyboard information page
    groupName   = ""
    information = ""

    # Maximum amount of registrations
    maxReg = 512

    # File extension (without leading dot)
    fileExt = ""

    # All known file extensions in a list
    allFileExtensions = []


    # Methods to be over-written...............................................

    def initEmptyFile(self):
        '''
        This method gets called by the default constructor. It's meant to be
        overwritten by sub-classes in order to initialize a new object as being
        an empty bank file.
        '''
        pass


    def initFromExistingFile(self, file):
        '''
        This method gets called by the default constructor. It's meant to be
        overwritten by sub-classes in order to initialize a new object from an
        existing bank file whise file object gets passed as argument.

        The most important taske to be carried out here is to extract all
        registrations from the given file, nicely pack them into Registration
        objects and to line them up in a list called self.regList.
        '''
        pass


    def storeBankFile(self, filename):
        '''
        This method stores the contents of self to a keyboard readable
        bank file.
        '''
        pass


    def canUnderstandFile(cls, file=None):
        '''
        A class method which checks whether the class can be used for
        accessing the given file's contents. A file object which can be
        read from gets passed to the method. Method must return either
        True or False.
        '''
        # Super-class doesn't support any file
        return False

    canUnderstandFile = classmethod(canUnderstandFile)


    # Default constructor .....................................................

    def __init__(self, filename="", file=None, keyboardName=""):
        '''
        Constructor. If neither a filename nor a file object is given a new
        bank file will be created in memory. If at least one is given the
        existing file will be used. If both are given the file object will
        be ignored.
        '''
        # Call super-constructor
        modelspecific.ModelSpecific.__init__(self, keyboardName=keyboardName)

        if not keyboardName:
            if file or filename:
                self.actualKeyboardName = self.__class__.getKeyboardNameFromFile(filename=filename, file=file)
            else:
                raise appexceptions.CannotDetermineKeyboardModel(self.__class__)

        # Initialize list of registration objects
        self.regList = []

        for i in range(self.__class__.maxReg):
            self.regList.append(None)

        # Call overridden initialization methods
        try:
            file = util.getFileObject(filename=filename, file=file)
            self.initFromExistingFile(file)
        except NoFileGiven:
            self.initEmptyFile()


    # Access to list of registration objects...................................

    def getRegistrationObjects(self):
        '''
        Extracts all registrations found in the bank file and returns a
        list registration objects containing those registrations. Empty
        registrations will be given as None.
        '''
        return self.regList


    def setRegistrationObjects(self, regList):
        '''
        Takes a list of registration objects and keeps it in memory. This
        method is the pendant to self.getRegistrationObjects() so the list
        must stick to the same format.

        Using self.storeBankFile() the contents of the list are stored to
        a keyboard readable bank file.
        '''
        # Store registration objects
        self.regList = regList

        # Fix list length
        missing = self.maxReg - len(regList)

        if missing > 0:
            for i in range(missing):
                self.regList.append(None)
        elif missing < 0:
            self.regList = self.regList[:self.maxReg]


    def createRegistrationObject(self, binary):
        '''
        Creates a Registration object from the given binary data. Makes sure
        that the right type of Registration objects gets created. Returns a
        new Registraion object on success or raises NoClassFound.
        '''
        # Search usable Registration class
        try:
            regClass = registration.Registration.getClassForKeyboardName(self.actualKeyboardName)
        except NoClassFound:
            raise NoClassFound()

        # Create new Registration object
        regObj = regClass(keyboardName=self.actualKeyboardName)
        regObj.setBinaryContent(binary)

        # Return newly created object
        return regObj


    # Lookup of suitable sub-class by bank file................................

    def hashFile(cls, file):
        '''
        A class method which generates hash code from the given file object.
        The hash code gets used for lookup of a sub-class which can handel the
        file. So on the one hand the hash code must be unique for each file of
        a different keyboard model but it must be identical within one model.
        As the hash function cannot be defined by the sub-classes the files
        leading 28 Byte get used which should in any case contain the file
        type's magic number.

        NOTE: A value greater than 28 Bytes will break PSR-2000 compatibility.
        Bytes 29-32 hold the amount of registrations in the PSR-2000 format.
        24 is minimum to detect a PSR-2000. But it's too much to detect Tyros
        style files.
        '''
        # Read up to 24 Bytes
        file.seek(0)
        return file.read(24)

    hashFile = classmethod(hashFile)


    def getClassForBankFile(cls, filename="", file=None):
        '''
        Class method which determines the class object of type BankFile which
        can handle the given file. The file can be given either by its filename
        or by a file object. If both are given the file object will be ignored.
        Raises appexceptions.UnknownKeyboardModel is no class can be found
        '''
        # Make sure to have a file object at hand
        file = util.getFileObject(filename, file)

        # Lookup suitable sub-class
        try:
            return cls.classFinderByFile.lookup(file)[0]
        except NoClassFound:
            raise appexceptions.UnknownKeyboardModel(cls)

    getClassForBankFile = classmethod(getClassForBankFile)


    def getKeyboardNameFromFile(cls, file=None, filename=""):
        '''
        A class method which determines the keyboard model of a give file.
        If the model can't be guessed an appexceptions.UnknownKeyboardModel
        exception gets raised. The file can be given either by its filename
        or by a file object. If both are given the file object will be ignored.
        '''
        # Super-class doesn't know of any keyboard model
        raise appexceptions.UnknownKeyboardModel(cls)

    getKeyboardNameFromFile = classmethod(getKeyboardNameFromFile)


    # Helper methods
    def getAllFileExtensions(cls):
        '''
        This static method returns a list of all known file extension. The
        list gets assembled by visiting all BankFile sub-classes
        '''
        # Return already existing list
        if cls.allFileExtensions:
            return cls.allFileExtensions

        # Visit BankFile-casses and build new list
        subClasses = cls.getAllSubclasses()

        for subClass in subClasses:
            extLow = subClass.fileExt.lower()

            if not extLow in cls.allFileExtensions:
                cls.allFileExtensions.append(extLow)

        # Return list
        return cls.allFileExtensions

    getAllFileExtensions = classmethod(getAllFileExtensions)
