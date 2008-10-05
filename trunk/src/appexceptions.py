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

This module provides all exceptions known in the main (psrregshuffle) package.
'''

# Public export of module content
__all__ = [
    "ClassIsSingleton",
    "NoClassObject",
    "NoClassFound",
    "NoFileGiven",
    "InvalidExportClass",
    "Cancel",
]


# Class definitions
class ExceptionWithMessage(Exception):
    '''
    This is a super-class for all self-defined exceptions which need to output
    a message on the call trace.
    '''

    _message = ""

    def __init__(self, data=None):
        '''
        Constructor. Takes the class object as optional parameter cls.
        '''
        pass

        ## NOTE: Commented since the data string doesn't help much and doesn't
        ## look nice in the excepthook dialog.
        # if data:
        #     self._message = "%s\n(%s)" % (self._message, str(data))


    def __str__(self):
        '''
        Returns string representation of the exception with a useful error
        message.
        '''
        return "%s" % (self._message)


class ClassIsSingleton(ExceptionWithMessage):
    '''
    This exception gets thrown whenever it's tried to instanciate a singleton
    class through one of its constructors instead of the dedicated accessor
    methods.
    '''

    _message = _("The object is a singleton object which shouldn't be instanciated through a constructor. Use getInstance() instead.")


class NoClassObject(ExceptionWithMessage):
    '''
    This exception gets thrown whenever a class object is expected for an
    argument but some other type was given.
    '''

    _message = _("The given object is not of type Class.")


class NoClassFound(ExceptionWithMessage):
    '''
    This exception gets thrown whenever the ClassFinder is unable to find
    a suitable class.
    '''

    _message = _("Couldn't find a suitable class. Most probably the feature is not implemented.")


class NoFileGiven(ExceptionWithMessage):
    '''
    This exception indicates that a method which usually takes a file name or
    a file object wasn't equiped with either.
    '''

    _message = _("No file was given at all when one was expected.")


class DoesNotMatchFilter(ExceptionWithMessage):
    '''
    Exception used by available registration display filter. Indicates a
    negative test result for a given entry.
    '''

    _message = _("The given registration doesn't match the given filter criterion.")

    def __init__(self, regEntry, Filter):
        '''
        Constructor. Takes regEntry and Filter model, too.
        '''
        self._message = "%s (%s, %s)" % (self._message, str(regEntry), str(Filter))


class InvalidExportClass(ExceptionWithMessage):
    '''
    Exception used to signal that a given class cannot export setlists.
    '''

    _message = _("Invalid export class given. The class must be a sub-class of ExportBase.")


class Cancel(ExceptionWithMessage):
    '''
    Exception used to signal that the user wishes to cancal a action.
    '''

    _message = _("The user wishes to cancel the current action.")
