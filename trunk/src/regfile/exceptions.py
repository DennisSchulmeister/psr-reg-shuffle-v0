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

#class ClassIsSingleton(Exception):
    #'''
    #This exception gets thrown whenever it's tried to instanciate a singleton
    #class through one of its constructors instead of the dedicated accessor
    #methods.
    #'''

    #_class   = None
    #_message = _("The object is a singleton object which shouldn't be instanciated through a constructor. Use getInstance() instead.")

    #def __init__(self, cls=None):
        #'''
        #Constructor. Takes the class object as optional parameter cls.
        #'''
        #self._class = cls

    #def __str__(self):
        #'''
        #Returns string representation of the exception with a useful error
        #message.
        #'''
        #return "%s (%s)" % (self._message, str(self._class))
