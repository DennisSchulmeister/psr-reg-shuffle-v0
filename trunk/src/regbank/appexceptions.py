#encoding=utf-8

# exceptions.py
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

This module provides all exceptions known in the regbank package.
'''

# Public export of module content
__all__ = [
    "UnknownKeyboardModel",
    "CannotDetermineKeyboardModel",
    "NoSubclassFound",
]


# Importing ExceptionWithMessage base-class
from ..appexceptions import ExceptionWithMessage


# Class definitions
class UnknownKeyboardModel(ExceptionWithMessage):
    '''
    This exception gets thrown whenever no BankFile or Registration class
    for a given keyboard model can be determined. Appearance of this class
    simply indicates that the keyboard model is not supported by the
    application.
    '''

    _message = _("Cannot handle data of the given keyboard model.")


class CannotDetermineKeyboardModel(ExceptionWithMessage):
    '''
    This exception gets thrown whenever it's tried to create a BankFile object
    without specifying either a keyboard name (for an initialy blank file) or
    giving an already existing file.
    '''

    _message = _("Neither keyboard model nor file given. Cannot create an empty object without hint about the keyboard model.")


class NameTooLong(ExceptionWithMessage):
    '''
    This exception indicates that a registration name exceeds to maximum
    limit set by the file format.
    '''

    _message = _("Name too long.")


    def __init__(self, name="", maxChars=0):
        '''
        Constructor which taks additional information.
        '''
        # Add given name to message
        if name:
            self._message += " %s: %s" % (_("Given name"), name)

        # Add max allowed length
        if maxChars:
            self._message += " %s: %i" % (_("Maximum allowed length"), maxChars)
