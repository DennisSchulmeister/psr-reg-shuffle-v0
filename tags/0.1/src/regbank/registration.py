#encoding=utf-8

# registration.py
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

This module contains the Registration class which is the base for all
model specific registration objects.
'''

# Public export of module content
__all__ = [
    "Registration"
]


# Import system modules
## TODO

# Import applicaiton modules
from .. import classfinder
from ..appexceptions import NoClassFound

import appexceptions


# Define Registration meta-class
class MetaRegistration(type):
    '''
    Meta-class for class Registration.
    '''

    def __init__(cls, name, bases, dict):
        '''
        Constructor. Called after class definition or class Registration.
        Injects a class attribute called "classFinder" for looking up suitable
        sub-classes by keyboard name.
        '''
        # Initialize class as usual
        super(MetaRegistration, cls).__init__(name, bases, dict)

        # Inject classFinder class attribute
        classFinder = classfinder.ClassFinder(
            superClass   = cls,
            classes      = __CLASSES__,
            testMethName = "canUnderstandKeyboardName",
            hashMethName = "hashKeyboardName"
        )
        setattr(cls, 'classFinder', classFinder)


# Define Registration class
class Registration:
    '''
    This class is the base for all model specific registration objects.
    '''

    # Meta-class for injecting ClassFinder object as class attribute.
    # NOTE: You cannot access the class object during definition of a class.
    # However the ClassFinder needs a super-class as an upper search limit so
    # a meta-class must be used in order to provide that information.
    __metaclass__ = MetaRegistration

    # Name of the keyboard model (needs to be overwritten)
    keyboardName = ""


    # Methods to be over-written...............................................

    def __init__(self):
        '''
        Default contructor.
        '''
        self.binaryContent = None


    def setName(self, name):
        '''
        Sets the name of the registration. If possible the name will be
        stored in the registration so that it appears on the keyboard screen.
        '''
        pass


    def getName(self):
        '''
        Returns the name of the registration. If possible the name as it
        appears on the keyboard screen will be given.
        '''
        pass


    # Access to binary data....................................................

    def setBinaryContent(self, binary):
        '''
        Sets the binary content of the registration. Usually this comes from
        a bank file or a registration file. This doesn't include the file
        header of a registration file. Just the registration as it's
        understood by the keyboard. (Without the bank file header either.)
        '''
        self.binaryContent = binary


    def getBinaryContent(self):
        '''
        Accesses the binary content of the registration. Usually this is needed
        for storing it to a bank file or to a registration file.
        '''
        return self.binaryContent


    # Lookup of suitable sub-class.............................................

    def getKeyboardName(self, name):
        '''
        Returns the name of the keyboard model for which the given registration
        is valid. This is usually needed for determining the file type of a
        bank file or a registration file to be written to disk.
        '''
        return self.__class__.keyboardName


    def canUnderstandKeyboardName(cls, name):
        '''
        Class method for checking whether a class can be used for manipulating
        data of the given keyboard make.
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
        Class method which determines the class object of type Registration
        which can handle registrations from the given keyboard model. Raises
        appexceptions.UnknownKeyboardModel is no class can be found.
        '''
        # Lookup suitable sub-class
        try:
            return cls.classFinder.lookup(keyboardName)
        except NoClassFound:
            raise appexceptions.UnknownKeyboardModel(cls)

    getClassForKeyboardName = classmethod(getClassForKeyboardName)
