#encoding=utf-8

# mainwindow.py
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

This module provides the main window class.
'''

# Import system modules
from kiwi.ui.delegates import GladeDelegate
import os.path

# Import application modules
import main


class MainWindow(GladeDelegate):
    '''
    This is the main window class.
    '''

    # List of controlled widgets
    widgets = []


    def __init__(self):
        '''
        Default constructor. Sets up the window but doesn't show it.
        '''
        # Calculate needed data
        # NOTE: Kiwi provides its own way of finding glade files. In fact
        # the main.dataDir has been added to Kiwi's search path by the main
        # singleton object so it's not needed here. Kiwi would ignore it
        # anway if the gladefile path was to include it.
        self.main = main.Main.getInstance()
        self.gladefile = "ui.glade"

        # Load glade file
        GladeDelegate.__init__(
            self,
            gladefile      = self.gladefile,
            toplevel_name  = "wndMain",
            delete_handler = self.quit_if_last
        )


    def run(self):
        '''
        Shows the main window and starts the main event loop.
        '''
        self.show_and_loop()
