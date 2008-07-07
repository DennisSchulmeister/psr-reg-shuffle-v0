#encoding=utf-8

# const.py
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

This module provides the main application class.
'''

# Import global modules
import optparse

# Import application modules
import exceptions
import const


class Main:
    '''
    This is the main application class. It's a singleton an provides global
    methods and variables. Note that global constants are defined in the
    module const.
    '''
    _singleton = None

    def getInstance(cls):
        '''
        This method needs to be used to access the singleton instance of this
        class. It makes sure that no two instances co-exist. For this to work
        you mustn't use the (default) constructor of the class.
        '''
        # Create new singleton if necessary
        if not isinstance(cls._singleton, cls):
            cls._singleton = cls(InternalUsage=True)

        # Return singleton
        return cls._singleton

    getInstance = classmethod(getInstance)


    def __init__(self, InternalUsage=False):
        '''
        Class constructor. Shouldn't never be explicitly used as the class
        resembles a singleton object.
        '''

        # Check for wrong usage of constructor instead of instance accessor
        if not InternalUsage:
            raise exceptions.ClassIsSingleton(self)

        # Store path of data directory as set by startup script
        self.dataDir = __PSR_DATA_DIR__

        # Prepare command line parser
        # HINT: Add option definitions here if necessary.
        self.parser = optparse.OptionParser(version=const.version_string)


    def run(self):
        '''
        This is the application's entry point. It gets called by the startup
        script. The script ../psr-reg-shuffle.py is meant for starting the
        system-wide installed version. However for development purposes its
        faster to start the local version without prior installation using
        ../start-dev-version.py.
        '''

        # Parse command line arguments
        # HINT: Don't add options here. Do so in __init__(...) instead.
        # But respond to given options here if necessay.
        (options, args) = self.parser.parse_args()

        print _("Welcome.")
