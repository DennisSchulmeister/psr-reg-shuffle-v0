#encoding=utf-8

# registration_psr2000.py
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
YAMAHA PSR-2000 registrations.
'''

# Public export of module content
__all__ = [
    "Registration_PSR2000"
]


# Import global modules
import struct
import codecs

# Import application modules
import registration
from .. import const
from .. import util


class Registration_PSR2000(registration.Registration):
    '''
    This class provides support for YAMAHA PSR-2000 registrations.
    '''

    # Short names of supported keyboard models
    keyboardNames = [const.YAMAHA_PSR2000]


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
        '''
        # Find position of GP00 Block (name of registration).
        # NOTE: Although the String "GP00" marks the begining of the
        # name block it is clever to search for "\xffGP00" since "GP00"
        # could also be part of a name itself. Also each GP00 seems to be
        # precent by several \xff characters.
        position = self.binaryContent.find("\xffGP00")

        if position < 0:
            return

        position += 1

        # Get maximum length of block
        length = self.binaryContent[position + 4 : position + 6]
        length = struct.unpack(">H", length)[0]

        # Skip block header
        position += 8
        length   -= 8

        # Decode name to latin_1
        if len(name) > length:
            shorten = length - len(name)
            name = name[:-shorten]

        asciiName = self.to_ascii(name) + (length - len(name)) * "\x00"

        # Insert name
        self.binaryContent = self.binaryContent[:position] \
                           + asciiName \
                           + self.binaryContent[position + length:]


    def getName(self):
        '''
        Returns the name of the registration. If possible the name as it
        appears on the keyboard screen will be given.
        '''
        # Find position of GP00 Block (name of registration).
        # NOTE: Although the String "GP00" marks the begining of the
        # name block it is clever to search for "\xffGP00" since "GP00"
        # could also be part of a name itself. Also each GP00 seems to be
        # precent by several \xff characters.
        position = self.binaryContent.find("\xffGP00")

        if position < 0:
            return ""

        position += 1

        # Get maximum length of block
        length = self.binaryContent[position + 4 : position + 6]
        length = struct.unpack(">H", length)[0]

        # Skip block header
        position += 8
        length   -= 8

        # Read name up to first \x00 character
        name = self.binaryContent[position : position + length]
        name = self.to_ucode(name)

        tail = name.find("\x00")

        if tail > -1:
            name = name[:tail]

        # Return extracted name
        return name
