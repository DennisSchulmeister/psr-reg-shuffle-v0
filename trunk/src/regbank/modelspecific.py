#encoding=utf-8

# modelspecific.py
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

This module contains a common base-class for Bankfile and Registration.
It inherits basic functionality needed in order to search classes by
keyboard model.
'''

# Public export of module content
__all__ = [
    "ModelSpecific"
]


# Import system modules
## TODO

# Import applicaiton modules
from .. import classfinder
from ..appexceptions import NoClassFound

import appexceptions


# Define ModelSpecific meta-class
class MetaModelSpecific(type):
    '''
    Meta-class for class ModelSpecific.
    '''

    def __init__(cls, name, bases, dict):
        '''
        Constructor. Called after class definition of class ModelSpecific.
        Injects a class attribute called "classFinderByName" for looking up
        suitable sub-classes by keyboard name.
        '''
        # Initialize class as usual
        super(MetaModelSpecific, cls).__init__(name, bases, dict)

        # Inject classFinder class attribute for search by keyboard name
        classFinder = classfinder.ClassFinder(
            superClass   = cls,
            classes      = __CLASSES__,
            testMethName = "canUnderstandKeyboardName",
            hashMethName = "hashKeyboardName"
        )
        setattr(cls, 'classFinderByName', classFinder)

        # Inject classFinder attribute for search of all sub-classes
        classFinder = classfinder.ClassFinder(
            superClass   = cls,
            classes      = __CLASSES__,
            testMethName = "testNoBaseClass",
            hashMethName = "hashClass"
        )
        setattr(cls, 'classFinderAllSubclasses', classFinder)


# Define base-class
class ModelSpecific:
    '''
    Base-class for Bankfile and Registration. Makes them searchable by
    keyboard model identifier.
    '''

    # Meta-class for injecting ClassFinder objects as class attribute.
    # NOTE: You cannot access the class object during definition of a class.
    # However the ClassFinders need a super-class as an upper search limit so
    # a meta-class must be used in order to provide that information.
    __metaclass__ = MetaModelSpecific

    # Short names of the supported keyboard models (needs to be overwritten)
    keyboardNames = []

    # User-information shown on the keyboard information page
    groupName   = ""
    information = ""


    def __init__(self, keyboardName=""):
        '''
        Default constructor. Remembers the actually used keyboard name. This
        is the model out of all supported which the object is supposed to
        assume.
        '''
        # Remember actualy used keyboard model
        self.actualKeyboardName = keyboardName


    # Lookup of suitable sub-class by keyboard model...........................

    def getKeyboardName(self):
        '''
        Returns a short string (up to 16 chars) of the keyboard model whose
        files are understood by the class.

        NOTE: This string is meant for being stored in registration files.
        It's purpose is to identify the class which can be used for editing
        the registration blocks and for assembling bank files.
        '''
        return self.actualKeyboardName


    def getAllKeyboardNames(cls):
        '''
        Returns a list of all supported keyboard models.
        '''
        return cls.keyboardNames

    getAllKeyboardNames = classmethod(getAllKeyboardNames)


    def canUnderstandKeyboardName(cls, name):
        '''
        A class method which checks whether the given name of the keyboard
        model belongs to it. Returns true if self.getKeyboardName returns
        the same string.
        '''
        return name in cls.keyboardNames

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
        appexceptions.UnknownKeyboardModel if no class can be found
        '''
        # Lookup suitable sub-class
        try:
            return cls.classFinderByName.lookup(keyboardName)[0]
        except NoClassFound:
            raise appexceptions.UnknownKeyboardModel(cls)

    getClassForKeyboardName = classmethod(getClassForKeyboardName)


    # Lookup of all sub-classes................................................

    def testNoBaseClass(cls, subclass):
        '''
        This test methods is used by the ClassFinderAllSubclasses object. In
        most cases it returns True, because the ClassFinder needs all
        candidates to give a positive test result. It returns False though
        if the base-class is tested in order to sort it out.
        '''
        return cls != subclass

    testNoBaseClass = classmethod(testNoBaseClass)


    def hashClass(cls, search):
        '''
        This method is used by the ClassFinderAllSubclasses object in order
        to hash the given classobject. This implementation simply returns
        the given value.
        '''
        return search

    hashClass = classmethod(hashClass)


    def getAllSubclasses(cls):
        '''
        Class method which uses a ClassFinder object in order to return a
        flat list of all subclasses of its class. Use this in order to get
        a list of all supported keyboard models by class.

        Doesn't catch the NoClassFound exception of the ClassFinder.
        '''
        return cls.classFinderAllSubclasses.lookup(cls)

    getAllSubclasses = classmethod(getAllSubclasses)
