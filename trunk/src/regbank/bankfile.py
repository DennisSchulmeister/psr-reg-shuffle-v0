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


# Import modules
import exceptions


# Define BankFile class
def BankFile(object):
    '''
    This is the base class which defines a common API for all classes dealing
    with bank files.
    '''

    # Class variables. Mostly constants
    keyboardName = ""                    # Short name of the keyboard model


    def __init__(self, filename="", file=None):
        '''
        Constructor. If neither a filename nor a file object is given a new
        bank file will be created in memory. If at least one is given the
        existing file will be used. If both are given the file object will
        be ignored.
        '''
        pass


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


    def getClassForKeyboardName(cls, name):
        '''
        Class method which determines the class object of type BankFile which
        can handle the given keyboard model. Raises
        exceptions.UnknownKeyboardModel is no class can be found
        '''
        raise exceptions.UnknownKeyboardModel()

    getClassForKeyboardName = classmethod(getClassForKeyboardName)


    def canUnderstandFile(cls, filename="", file=None):
        '''
        A class method which checks whether the class can be used for
        accessing the given file's contents. The file can be given either
        by its filename or by a file object. If both are given the file
        object will be ignored.
        '''
        return False

    canUnderstandFile = classmethod(canUnterstandFile)


    def getClassForBankFile(cls, filename="", file=None):
        '''
        Class method which determines the class object of type BankFile which
        can handle the given file. The file can be given either by its filename
        or by a file object. If both are given the file object will be ignored.
        Raises exceptions.UnknownKeyboardModel is no class can be found
        '''
        raise exceptions.UnknownKeyboardModel()

    getClassForBankFile = classmethod(getClassForBankFile)


    def getRegistrationObjects(self):
        '''
        Extracts all registrations found in the bank file and returns a
        list registration objects containing those registrations. Empty
        registrations will be given as None.
        '''
        return [None, None, None, None, None, None, None, None]


    def setRegistrationObjects(self, regList):
        '''
        Takes a list of registration objects and keeps it in memory. This
        method is the pendant to self.getRegistrationObjects() so the list
        must stick to the same format.

        Using self.storeBankFile() the contents of the list are stored to
        a keyboard readable bank file.
        '''
        pass


    def storeBankFile(self, filename):
        '''
        This method stores the contents of self to a keyboard readable
        bank file.
        '''
        pass
