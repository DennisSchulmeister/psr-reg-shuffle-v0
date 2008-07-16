#encoding=utf-8

# Registration.py
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

class Registration(object):
    '''
    This class is the base for all model specific registration objects.
    '''

    def __init__(self):
        '''
        Default contructor.
        '''
        self.binaryContent = None
        self.keyboardName  = ""
        pass

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

    def setKeyboardName(self, name):
        '''
        Sets the name of the keyboard model for which the given registration
        is valid. This information usually comes from a bank file or a
        registration file together with its binary content.
        '''
        self.keyboardName = name

    def getKeyboardName(self, name):
        '''
        Returns the name of the keyboard model for which the given registration
        is valid. This is usually needed for determining the file type of a
        bank file or a registration file to be written to disk.
        '''
        return self.keyboardName

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
