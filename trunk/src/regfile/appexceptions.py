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

This module provides all exceptions known in the regfile package.
'''

# Public export of module content
__all__ = [
    "UnknownFileFormat"
]


# Importing ExceptionWithMessage base-class
from ..appexceptions import ExceptionWithMessage


class UnknownFileFormat(ExceptionWithMessage):
    '''
    This exception indicates that it was tried to open an invalid
    registration file.
    '''

    _message = _("The given file doesn't seem to be a registration file. Note that registration files hold only one registration as opposed to registration banks used by your instrument.")
