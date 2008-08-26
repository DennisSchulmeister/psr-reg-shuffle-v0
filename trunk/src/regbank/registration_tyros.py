#encoding=utf-8

# registration_tyros.py
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

This module contains the Registration class which provides support for
YAMAHA Tyros and Tyros 2 registrations.
'''

# Public export of module content
__all__ = [
    "Registration_Tyros"
]


# Import global modules
import struct
import codecs

# Import application modules
import registration
from .. import const
from .. import util


class Registration_Tyros(registration.Registration):
    '''
    This class provides support for YAMAHA Tyros and Tyros 2 registrations.
    '''

    # Short names of supported keyboard models
    keyboardNames = [
        const.YAMAHA_TYROS1,
        const.YAMAHA_TYROS2,
        const.YAMAHA_S900,
        const.YAMAHA_S700,
        const.YAMAHA_PSR3000,
    ]


    # Object creation..........................................................

    def __init__(self, keyboardName=""):
        '''
        Default contructor.
        '''
        # Call super-constructor
        registration.Registration.__init__(self, keyboardName)

        # Retrieve ascii encoder / decoder
        self.encoder  = codecs.getencoder("ascii")
        self.decoder  = codecs.getdecoder("ascii")

        self.to_ascii = lambda t: self.encoder(t)[0]
        self.to_ucode = lambda t: self.decoder(t)[0]


    # Static helper methods....................................................

    def stripName(cls, name=""):
        '''
        This method needs to be reimplemented by subclasses. It's meant to
        remove file extions and other non-name data (like icons) from name
        strings.
        '''
        return util.stripNameYamaha(
            name    = name
        )

    stripName = classmethod(stripName)


    # Data access..............................................................

    def setName(self, name):
        '''
        Sets the name of the registration. If possible the name will be
        stored in the registration so that it appears on the keyboard screen.

        NOTE: Unlike previous file formats (PSR-2000) the name string is
        not null-terminated anymore. Instead of the block length the length
        now gives the exact string length (2-Byte Big Endian, unsigned int).
        '''
        # Find position of GPm\x01 Block (name of registration).
        position = self.binaryContent.find("GPm\x01")

        if position < 0:
            return

        # Get old string length
        oldLength = self.binaryContent[position + 4 : position + 6]
        oldLength = struct.unpack(">H", oldLength)[0]

        # Calculate new length bytes
        length = len(name)
        lengthBytes = struct.pack(">H", length)

        # Decode name to latin_1
        asciiName = self.to_ascii(name)

        # Insert name
        self.binaryContent = self.binaryContent[:position] \
                           + "GPm\x01" \
                           + lengthBytes \
                           + asciiName \
                           + self.binaryContent[position + 6 + oldLength:]

        # Update global length bytes
        self.updateLengthBytes()


    def getName(self):
        '''
        Returns the name of the registration. If possible the name as it
        appears on the keyboard screen will be given.

        NOTE: Unlike previous file formats (PSR-2000) the name string is
        not null-terminated anymore. Instead of the block length the length
        now gives the exact string length. (2-Byte Big Endian, unsigned int)
        '''
        # Find position of GPm\x01 Block (name of registration).
        position = self.binaryContent.find("GPm\x01")

        if position < 0:
            return ""

        # Get string length
        length = self.binaryContent[position + 4 : position + 6]
        length = struct.unpack(">H", length)[0]

        # Skip block header
        position += 6

        # Read name of given length
        name = self.binaryContent[position : position + length]
        name = self.to_ucode(name)

        # Return extracted name
        return name


    def updateLengthBytes(self):
        '''
        Each registration contains a two-byte length field which needs to be
        updated after every other change. This is done by this method.

        ===== ====== ==========================================================
        Start Length Description
        ===== ====== ==========================================================
        0     4      Registration magic number (BHd\x00)
        4     2      Big-endian length byte (without header!)
        6     ...    Registration data
        ===== ====== ==========================================================
        '''
        # Calculate length bytes
        length = len(self.binaryContent) - 6         # Without header = 6 Bytes
        lengthBytes = struct.pack(">H", length)

        # Calculate new registration header
        regHeader = "BHd\x00" + lengthBytes

        # Replace header
        self.binaryContent = regHeader + self.binaryContent[6:]
