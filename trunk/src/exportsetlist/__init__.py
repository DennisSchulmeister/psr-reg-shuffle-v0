#encoding=utf-8

# __init__.py
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

This module provides classes for exporting (and printing) the contents of
bank files given as a list of BankFile objects.
'''

# Imports
import __builtin__
import types

import os.path
import os


# Public export of module content
__all__ = [
  "classes"
]


# Get all modules except __init__.py
modPath = os.path.dirname(os.path.join(os.getcwd(), __file__))
classes = []

# Visit each module and get classes
__builtin__.__dict__["__EXPORT_CLASSES__"] = classes

for filename in os.listdir(modPath):
    (base, ext) = os.path.splitext(filename)

    if ext == ".py" and not base == "__init__":
        # Import module
        try:
            exec("import %s" % (base))
        except SyntaxError:
            pass

        # Get list of classes
        try:
            exec("mod = %s" % (base))

            for name in dir(mod):
                thing = getattr(mod, name)

                if thing and isinstance(thing, (type, types.ClassType)):
                    classes.append(thing)

        except SyntaxError:
            pass
