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


# Define BankFile meta-class
class MetaBankFile(type):
    '''
    Meta-class for class Registration.
    '''

    def __init__(cls, name, bases, dict):
        '''
        Constructor. Called after class definition or class BankFile.
        Injects class attributes "classFinderByName" and "classFinderByFile"
        for looking up suitable sub-classes by keyboard name and bank file.
        '''
        # Initialize class as usual
        super(MetaBankFile, cls).__init__(name, bases, dict)

        # Inject classFinder class attributes
        classFinderByName = classfinder.ClassFinder(
            superClass   = cls,
            packagePath  = __file__,
            testMethName = "canUnderstandKeyboardName",
            hashMethName = "hashKeyboardName"
        )
        setattr(cls, 'classFinderByName', classFinderByName)

        classFinderByFile = classfinder.ClassFinder(
            superClass   = cls,
            packagePath  = __file__,
            testMethName = "canUnderstandFile",
            hashMethName = "hashFile"
        )
        setattr(cls, 'classFinderByFile', classFinderByFile)


# Define BankFile class
class BankFile:
    '''
    This is the base class which defines a common API for all classes dealing
    with bank files.
    '''

    # Meta-class for injecting ClassFinder objects as class attribute.
    # NOTE: You cannot access the class object during definition of a class.
    # However the ClassFinders need a super-class as an upper search limit so
    # a meta-class must be used in order to provide that information.
    __metaclass__ = MetaBankFile

    # Short name of the keyboard model
    keyboardName = ""

    # Maximum amount of registrations
    maxReg = 512


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

    def __init__(self, filename="", file=None):
        '''
        Constructor. If neither a filename nor a file object is given a new
        bank file will be created in memory. If at least one is given the
        existing file will be used. If both are given the file object will
        be ignored.
        '''
        # Initialize list of registration objects
        self.regList = [None, None, None, None, None, None, None, None]

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


    def createRegistrationObject(self, binary):
        '''
        Creates a Registration object from the given binary data. Makes sure
        that the right type of Registration objects gets created. Returns a
        new Registraion object on success or raises NoClassFound.
        '''
        # Search usable Registration class
        try:
            regClass = registration.Registration.getClassForKeyboardName(self.__class__.keyboardName)
        except NoClassFound:
            raise NoClassFound()

        # Create new Registration object
        regObj = regClass()
        regObj.setBinaryContent(binary)

        # Return newly created object
        return regObj



    # Lookup of suitable sub-class by keyboard name............................

    def getKeyboardName(cls):
        '''
        Returns a short string (up to 16 chars) of the keyboard model whose
        files are understood by the class.

        NOTE: This string is meant for being stored in registration files.
        It's purpose is to identify the class which can be used for editing
        the registration blocks and for assembling bank files.
        '''
        return cls.keyboardName

    getKeyboardName = classmethod(getKeyboardName)


    def canUnderstandKeyboardName(cls, name):
        '''
        A class method which checks whether the given name of the keyboard
        model belongs to it. Returns true if self.getKeyboardName returns
        the same string.
        '''
        return name == cls.keyboardName

    canUnderstandKeyboardName = classmethod(canUnderstandKeyboardName)


    def hashKeyboardName(cls, name):
        '''
        Hash function for keyboard name. Needed for class lookup below.
        Since keyboard names are short and unique just the given name will be
        returned.
        '''
        return name

    hashKeyboardName = classmethod(hashKeyboardName)


    def getClassForKeyboardName(cls, keyboardName):
        '''
        Class method which determines the class object of type BankFile which
        can handle the given keyboard model. Raises
        appexceptions.UnknownKeyboardModel is no class can be found
        '''
        # Lookup suitable sub-class
        try:
            return cls.classFinderByName.lookup(keyboardName)
        except NoClassFound:
            raise appexceptions.UnknownKeyboardModel(cls)

    getClassForKeyboardName = classmethod(getClassForKeyboardName)


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
        '''
        # Read up to 28 Bytes
        file.seek(0)
        return file.read(28)

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
            return cls.classFinderByFile.lookup(file)
        except NoClassFound:
            raise appexceptions.UnknownKeyboardModel(cls)

    getClassForBankFile = classmethod(getClassForBankFile)
