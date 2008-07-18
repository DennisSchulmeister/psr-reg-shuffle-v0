#encoding=utf-8

# regFile.py
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

This module contains the RegFile class which defines a container file format
for registration objects. Each registration file hold one registration
object.
'''

# Public export of module content
__all__ = [
    "RegFile"
]


class RegFile:
    '''
    Class for using registration files.
    '''

    def __init__(self, filename="", file=None):
        '''
        Constructor. Either opens an existing file by taking its filename
        or file object or creates a new one in memory if none of these is
        given. If both are given a new file object will be created.
        '''
        pass


    def canUnderstandFile(cls, filename="", file=None):
        '''
        A class method for checking whether the given file is a valid
        registration file. File can be given either by its path (filename) or
        by a file object. If both is given the file object will be ignored.
        '''
        return False

    canUnderstandFile = classmethod(canUnderstandFile)


    def getKeyboardName(self):
        '''
        Returns the name of the keyboard model of this file. This is the
        same string as it gets stored in the file.
        '''
        return ""


    def setKeyboardName(self, name):
        '''
        Sets the name of the keyboard model.
        '''
        pass


    def getRegistrationObject(self):
        '''
        Extracts a registration object from the file.
        '''
        return None


    def setRegistrationObject(self, regObject):
        '''
        Inserts a registration object into the file and replaces a previously
        existing one.
        '''
        pass


    def storeRegFile(self, filename):
        '''
        Stores the file to disk using the given path (filename).
        '''
        pass
