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
import os
import os.path
import types
import glob
import sys

# Import applicaiton modules
import exceptions


# Define Registration class
class Registration(object):
    '''
    This class is the base for all model specific registration objects.
    '''

    # Name of the keyboard model
    keyboardName = "ABC"


    def __init__(self):
        '''
        Default contructor.
        '''
        self.binaryContent = None


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


    def getClassForKeyboardName(cls, keyboardName):
        '''
        Class method which determines the class object of type Registration
        which can handle registrations from the given keyboard model. Raises
        exceptions.UnknownKeyboardModel is no class can be found
        '''
        # Calculate package name
        global __file__

        (dir, dummy) = os.path.split(__file__)
        dir = dir.replace(os.path.commonprefix([dir, os.getcwd()]), "")

        if dir.startswith(os.sep):
            dir = dir[1:]

        packageName  = dir.replace(os.sep, ".")

        # Import and check each module file of package directory
        globPattern = os.path.join(dir, "*.py")
        foundClass  = None

        for filename in glob.glob(globPattern):
            # Calculate module name from file name
            (dummy, moduleName) = os.path.split(filename)
            moduleName = "%s.%s" % (packageName, moduleName[:-3])

            # Import module
            module = __import__(name=moduleName, fromlist=[packageName])

            if not module or not hasattr(module, "__all__"):
                continue

            # Browser module members for subclasses of Registration
            for name in module.__all__:
                # Get member object from name
                member = getattr(module, name)

                # Only process sub-classes of Registration
                if not isinstance(member, (type, types.ClassType)) \
                or not issubclass(member, cls):
                    continue

                # Query class whether it feels suitable
                if member.canUnderstandKeyboardName(keyboardName):
                    foundClass = member
                    break

            # Delete module
            del(module)

            # Return if a suitable class has been found.
            if foundClass:
                return foundClass

        # No class found. Raise exception
        raise exceptions.UnknownKeyboardModel()

    getClassForKeyboardName = classmethod(getClassForKeyboardName)


    def setName(self, name):
        '''
        Sets the name of the registration. If possible the name will be
        stored in the registration so that it appears on the keyboard screen.
        '''
        pass


    def getName(self, name):
        '''
        Returns the name of the registration. If possible the name as it
        appears on the keyboard screen will be given.
        '''
        pass
