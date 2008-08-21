#encoding=utf-8

# bankfile_psr2000.py
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
bank files from the YAMAHA PSR-2000 keyboard.
'''

# Public export of module content
__all__ = [
    "BankFile_PSR2000"
]


# Import global modules
import struct

# Import application modules
import bankfile
from .. import const
from .. import util


# Define class
class BankFile_PSR2000(bankfile.BankFile):
    '''
    This class provides support for YAMAHA PSR-2000 bank files.
    '''

    # Short names of supported keyboard models
    keyboardNames = [const.YAMAHA_PSR2000]

    # User-information shown on the keyboard information page
    groupName   = _("Yamaha PSR-2000 and alike")
    information = _("Released in 2001 the Yamaha PSR-2000 marks the end of the highly successful PSR-9000 line. It shares many features of its big brothers the PSR-9000 and 9000pro, among them most sounds, styles and a very similar albeit updated operating system. Updates include a largely re-designed main screen, notation display as well as icons next to each object name (with the icon descriptor being a sufix to the name).")

    # Maximum amount of registrations
    maxReg = 8

    # File extension
    fileExt = "reg"

    # Magic file header
    fileHeader = "\x52\x45\x47\x2D\x31\x30\x30\x2D" \
               + "\x31\x30\x30\x2D\x31\x30\x30\x30" \
               + "\x50\x53\x52\x32\x30\x30\x30\x78" \
               + "\x00\x08\x00\x40"

    # Special padding between header and data blocks
    specialPadding = "\x24\xFF\xFF\xFF\xFF\xFF\xFF\xFF" \
                   + "\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF" \
                   + "\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF" \
                   + "\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF" \
                   + "\xFF\xFF\xFF\xFF\xFF\x00\x00\x00" \
                   + "\x00\x00\x00\x00\x00\x00\x00\x00"


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
        # Slice out registrations into self.regList
        # NOTE: 0xffffffff marks non-existing registration. Other values
        # give absolute byte pointer within file.
        for i in range(self.__class__.maxReg):
            # Read location of registration
            file.seek(32 + (4 * i))
            startPos = file.read(4)

            # Skip empty registrations
            if startPos == "\xff\xff\xff\xff":
                continue

            # Read length of registration block
            start = struct.unpack(">I", startPos)[0]
            file.seek(start + 6)                          # RGST01..

            blockLength = file.read(2)
            length      = struct.unpack(">H", blockLength)[0]

            # Slice out binary data of registration
            file.seek(start)
            binary = file.read(length)

            # Create Registration object and put it into the list
            self.regList[i] = self.createRegistrationObject(binary)


    # File access..............................................................

    def storeBankFile(self, filename):
        '''
        This method stores the contents of self to a keyboard readable
        bank file.

        File format is as follows:

        ========= ======= =====================================================
        Position  Length  Description
        ========= ======= =====================================================
        0         28      File header
        28        4       Amount of registrations
        32        32      Access list with location of registration (8x)
        64        48      Special padding
        112       ..      Registration blocks (up to 8x)
        ========= ======= =====================================================

        All numbers are stored as BigEndian, 4-Byte, Unsigned Integer.
        '''
        # Prepare access list and large data block
        nRegs      = 0
        startPosi  = 112
        accessList = ""
        dataBlock  = ""

        for reg in self.regList:
            # Skip empty registrations
            if not reg:
                accessList += "\xFF\xFF\xFF\xFF"
                continue

            # Determine effective amount of registrations
            nRegs += 1

            # Write access list and update location for next registration
            posi = startPosi + len(dataBlock)

            accessList += struct.pack(">I", posi)     # BE, UInt, 4 Bytes
            dataBlock  += reg.getBinaryContent()

        # Write file contents
        file = open(filename, "wb+")
        file.write(self.__class__.fileHeader)         # File header
        file.write(struct.pack("<I", nRegs))          # Amount of registrations (LE???)
        file.write(accessList)                        # Location pointers
        file.write(self.__class__.specialPadding)     # Special padding
        file.write(dataBlock)                         # Registration block
        file.close()


    def canUnderstandFile(cls, file=None):
        '''
        A class method which checks whether the class can be used for
        accessing the given file's contents. A file object which can be
        read from gets passed to the method. Method must return either
        True or False.
        '''
        # Compare file header
        headerSize = len(cls.fileHeader)

        file.seek(0)
        fileHeader = file.read(headerSize)

        return fileHeader == cls.fileHeader

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

        if cls.canUnderstandFile(file=file):
            return const.YAMAHA_PSR2000
        else:
            raise appexceptions.UnknownKeyboardModel(cls)

    getKeyboardNameFromFile = classmethod(getKeyboardNameFromFile)
