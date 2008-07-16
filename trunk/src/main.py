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
import gobject
import kiwi.environ
import os.path
import os

# Import application modules
import mainwindow
import exceptions
import const


class Main(gobject.GObject):
    '''
    This is the main application class. It's a singleton an provides global
    methods and variables. Note that global constants are defined in the
    module const.

    Emited signals:
    ---------------

    *work-dir-changed:* The working directory has been changed. The new
    directory is given as soley parameter to the signal.
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

        # Add data directory to kiwi's list of resource paths.
        # NOTE: Kiwi provides its own way of finding resources like glade
        # files and images which can also distinguish between running an
        # installed or an uninstalled version of the application. In future
        # it might be wise to better use that feature instead of the dataDir
        # as determined by two seperate startup scripts.
        if os.path.exists(self.dataDir) and os.path.isdir(self.dataDir):
            kiwi.environ.environ.add_resource("glade", self.dataDir)

        # Prepare command line parser
        # HINT: Add option definitions here if necessary.
        self.parser = optparse.OptionParser(version=const.version_string)

        # Define work-dir-changed signal
        gobject.GObject.__init__(self)

        gobject.signal_new(
            "work-dir-changed",
            Main,
            gobject.SIGNAL_RUN_LAST,
            gobject.TYPE_NONE,
            (gobject.TYPE_STRING,)
        )

        # Add additional instance variables
        self.workDir = os.getcwd()


    def run(self):
        '''
        This is the application's entry point. It gets called by the startup
        script. The script ../psr-reg-shuffle.py is meant for starting the
        system-wide installed version. However for development purposes its
        faster to start the local version without prior installation using
        ../start-dev-version.py.
        '''

        # Parse command line arguments
        # HINT: Don't add options here. Do so in __init__(self, ...) instead.
        # But respond to given options here if necessay.
        (options, args) = self.parser.parse_args()

        # Show main window
        self.wnd = mainwindow.MainWindow()
        self.wnd.run()


    def setWorkDir(self, workDir):
        '''
        This method should be used for changing the work directory instead
        of direct manipulation of the instance variable workDir. The method
        has the advantage that it checks for a valid path and that it emits
        the work-dir-changed signal for letting other objects know about the
        change.
        '''
        # Check whether a valid directory was given
        if not os.path.exists(workDir) or not os.path.isdir(workDir):
            return

        # Change work directory
        self.workDir = workDir

        # Emit work-dir-changed signal
        self.emit("work-dir-changed", self.workDir)
