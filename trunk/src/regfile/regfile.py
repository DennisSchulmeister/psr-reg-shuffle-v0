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

# Import application modules
from .. import util
from ..regbank import registration

import appexceptions

# Import system modules
import codecs


# Class definition
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
        # Retrieve ascii encoder / decoder
        self.encoder  = codecs.getencoder("ascii")
        self.decoder  = codecs.getdecoder("ascii")

        self.to_ascii = lambda t: self.encoder(t)[0]
        self.to_ucode = lambda t: self.decoder(t)[0]

        # Initialize attributes
        self.keyboardName = ""
        self.regObj = None


        # Import file if given
        if file or filename:
            # Open file for reading
            file = util.getFileObject(filename=filename, file=file)

            # Check for valid file
            if not self.__class__.canUnderstandFile(file=file):
                file.close()
                raise appexceptions.UnknownFileFormat()

            # Read keyboard name
            file.seek(4)
            self.keyboardName = file.read(16)
            self.keyboardName = self.to_ucode(self.keyboardName)
            tail = self.keyboardName.find("\x00")

            if tail > -1:
                self.keyboardName = self.keyboardName[:tail]

            # Read registration block
            file.seek(20)
            regBinary = file.read()

            regClass    = registration.Registration.getClassForKeyboardName(self.keyboardName)
            self.regObj = regClass(keyboardName=self.keyboardName)

            self.regObj.setBinaryContent(regBinary)


    def canUnderstandFile(cls, filename="", file=None):
        '''
        A class method for checking whether the given file is a valid
        registration file. File can be given either by its path (filename) or
        by a file object. If both is given the file object will be ignored.
        '''
        # Get temporary decoder
        decoder  = codecs.getdecoder("ascii")
        to_ucode = lambda t: decoder(t)[0]

        # Open file for reading
        file = util.getFileObject(filename=filename, file=file)

        # Check for valid file
        file.seek(0)
        magic = file.read(4)
        magic = to_ucode(magic)

        return magic == "RS01"

    canUnderstandFile = classmethod(canUnderstandFile)


    def storeRegFile(self, filename):
        '''
        Stores the file to disk using the given path (filename).
        '''
        # Open file for writing
        file = open(filename, "wb+")

        # Prepare file content
        magic     = self.to_ascii("RS01")
        keyName   = self.to_ascii(self.keyboardName) \
                  + (16 - len(self.keyboardName)) * "\x00"
        regBinary = self.regObj.getBinaryContent()

        # Write file
        file.seek(0)
        file.write(magic)
        file.write(keyName)
        file.write(regBinary)

        # Close file
        file.close


    def getKeyboardName(self):
        '''
        Returns the name of the keyboard model of this file. This is the
        same string as it gets stored in the file.
        '''
        return self.keyboardName


    def setKeyboardName(self, name):
        '''
        Sets the name of the keyboard model.
        '''
        self.keyboardName = name


    def getRegistrationObject(self):
        '''
        Extracts a registration object from the file.
        '''
        return self.regObj


    def setRegistrationObject(self, regObj):
        '''
        Inserts a registration object into the file and replaces a previously
        existing one.
        '''
        self.regObj = regObj
