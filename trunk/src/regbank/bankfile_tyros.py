#encoding=utf-8

# bankfile_tyros.py
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

This module contains the BankFile sub-class for dealing with registration
bank files from the YAMAHA Tyros and Tyros 2 keyboards.
'''

# Public export of module content
__all__ = [
    "BankFile_Tyros"
]


# Import global modules
import struct

# Import application modules
import bankfile
from .. import const
from .. import util


# Define class
class BankFile_Tyros(bankfile.BankFile):
    '''
    This class provides support for YAMAHA Tyros and Tyros 2 bank files.
    '''

    # Short names of supported keyboard models
    keyboardNames = [
        const.YAMAHA_TYROS1,
        const.YAMAHA_TYROS2,
        const.YAMAHA_S900,
        const.YAMAHA_S700,
        const.YAMAHA_PSR3000,
    ]

    # User-information shown on the keyboard information page
    groupName   = _("Yamaha Tyros descendants")
    information = _("The Yamaha Tyros holds as a milestone for a new generation of Yamaha's top- and mid-level arranger keyboards. Being loosely based upon its predecessors it introduced a new technical platform as a base for much offspring. Those models share very similar file formats which is why they are assumed to be able to read each-other's data.")

    # Maximum amount of registrations
    maxReg = 8

    # File extension
    fileExt = "rgt"

    # Magic file headers
    fileHeaders = {
        const.YAMAHA_TYROS1:  "\x53\x70\x66\x46\x00\x10\x0A\xD9" \
                              "\x52\x47\x53\x54\x00\x00\x00\x07",

        const.YAMAHA_TYROS2:  "\x53\x70\x66\x46\x00\x10\x0B\x75" \
                              "\x52\x47\x53\x54\x00\x02\x00\x00",

        const.YAMAHA_S900:    "\x53\x70\x66\x46\x00\x10\x0B\xC6" \
                              "\x52\x47\x53\x54\x00\x02\x00\x00",

        const.YAMAHA_S700:    "\x53\x70\x66\x46\x00\x10\x0B\xC7" \
                              "\x52\x47\x53\x54\x00\x02\x00\x00",

        const.YAMAHA_PSR3000: "\x53\x70\x66\x46\x00\x10\x0B\x20" \
                              "\x52\x47\x53\x54\x00\x01\x00\x02",
    }

    # File footer
    fileFooter = "\x46\x45\x6E\x64\x00\x00"        # FEnd\x00\x00

    # Special padding between header and data blocks
    specialPaddings = {
        const.YAMAHA_TYROS1:  "\x15\x5C" \
                              "\x42\x48\x64\x01\x00\x24\xFF\xFF" \
                              "\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF" \
                              "\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF" \
                              "\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF" \
                              "\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF" \
                              "\xFF\xFF",

        const.YAMAHA_TYROS2:  "\x00\x82" \
                              "\x42\x48\x64\x01\x00\x24\xFF\xFF" \
                              "\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF" \
                              "\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF" \
                              "\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF" \
                              "\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF" \
                              "\xFF\xFF",

        const.YAMAHA_S900:    "\x00\x78" \
                              "\x42\x48\x64\x01\x00\x24\x00\x01" \
                              "\xFF\x04\x05\x06\x07\xFF\x00\x00" \
                              "\x00\x00\x00\x00\x00\x00\x00\x00" \
                              "\x00\x00\x00\x00\x00\x00\x00\x00" \
                              "\x00\x00\x00\x00\x00\x00\x00\x00" \
                              "\x00\x00",

        const.YAMAHA_S700:    "\x00\x66" \
                              "\x42\x48\x64\x01\x00\x24\xFF\xFF" \
                              "\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF" \
                              "\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF" \
                              "\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF" \
                              "\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF" \
                              "\xFF\xFF",

        const.YAMAHA_PSR3000: "\x00\x00" \
                              "\x42\x48\x64\x01\x00\x24\xFF\xFF" \
                              "\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF" \
                              "\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF" \
                              "\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF" \
                              "\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF" \
                              "\xFF\xFF",
    }


    # Object initialization....................................................
    def __init__(self, filename="", file=None, keyboardName=""):
        '''
        Constructor. If neither a filename nor a file object is given a new
        bank file will be created in memory. If at least one is given the
        existing file will be used. If both are given the file object will
        be ignored.
        '''
        # Initialize object from super-constructor
        bankfile.BankFile.__init__(self, filename=filename, file=file, keyboardName=keyboardName)


    def initEmptyFile(self):
        '''
        This method gets called by the default constructor. It's meant to be
        overwritten by sub-classes in order to initialize a new object as being
        an empty bank file.
        '''
        # Nothing to do
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
        # Start with empty registration list
        self.regList = []

        # Slice out registrations into self.regList
        # NOTE: Empty (non-existing) registrations are stored as reigstrions
        # with zero-size.
        file.seek(64)

        while True:
            # Check for adjacent registration block
            blockMagic = file.read(4)

            if not blockMagic == "BHd\x00":
                break

            # Read block length
            blockLength = file.read(2)
            length      = struct.unpack(">H", blockLength)[0]

            # Slice out binary data and create registration object
            if length > 0:
                binary = blockMagic + blockLength + file.read(length)
                regObj = self.createRegistrationObject(binary)
            else:
                regObj = None

            # Put registration object into the list
            self.regList.append(regObj)


    # File access..............................................................

    def storeBankFile(self, filename):
        '''
        This method stores the contents of self to a keyboard readable
        bank file.

        File format is as follows:

        ========= ======= =====================================================
        Position  Length  Description
        ========= ======= =====================================================
        0         16      File header
        16        4       File-size in bytes
        20        44      Special Padding (BHd\x01 block)
        64        --      Exactly 8 registration blocks of variable length
        -6        6       File footer
        ========= ======= =====================================================

        All numbers are stored as BigEndian, 4-Byte, Unsigned Integer.
        '''
        # Prepare data block with registration data
        dataBlock  = ""

        for regObj in self.regList:
            if not regObj:
                dataBlock += "BHd\x00\x00\x00"
            else:
                dataBlock += regObj.getBinaryContent()

        # Calculate file length
        header  = self.__class__.fileHeaders[self.actualKeyboardName]
        padding = self.__class__.specialPaddings[self.actualKeyboardName]
        footer  = self.__class__.fileFooter

        length      = len(header) + 4 + len(padding) + len(dataBlock) + len(footer)
        lengthBytes = struct.pack(">I", length)

        # Write file contents
        file = open(filename, "wb+")
        file.write(header)               # File header
        file.write(lengthBytes)          # File-size (4-Byte uint, BE)
        file.write(padding)              # Special padding (BHd\x01 block)
        file.write(dataBlock)            # Registration data
        file.write(footer)               # File footer
        file.close()


    def canUnderstandFile(cls, file=None):
        '''
        A class method which checks whether the class can be used for
        accessing the given file's contents. A file object which can be
        read from gets passed to the method. Method must return either
        True or False.
        '''
        # Compare file header
        hit = False

        for keyName in cls.fileHeaders:
            testHeader = cls.fileHeaders[keyName]
            headerSize = len(testHeader)

            file.seek(0)
            fileHeader = file.read(headerSize)

            if fileHeader == testHeader:
                hit = True
                break

        return hit

    canUnderstandFile = classmethod(canUnderstandFile)


    def getKeyboardNameFromFile(cls, file=None, filename=""):
        '''
        A class method which determines the keyboard model of a give file.
        If the model can't be guessed an appexceptions.UnknownKeyboardModel
        exception gets raised. The file can be given either by its filename
        or by a file object. If both are given the file object will be ignored.
        '''
        # Make sure to have a file object at hand
        file = util.getFileObject(filename, file)

        # Compare file header
        foundKeyName = ""

        for keyName in cls.fileHeaders:
            testHeader = cls.fileHeaders[keyName]
            headerSize = len(testHeader)

            file.seek(0)
            fileHeader = file.read(headerSize)

            if fileHeader == testHeader:
                foundKeyName = keyName
                break

        # Return result
        if foundKeyName:
            return foundKeyName
        else:
            raise appexceptions.UnknownKeyboardModel(cls)

    getKeyboardNameFromFile = classmethod(getKeyboardNameFromFile)
