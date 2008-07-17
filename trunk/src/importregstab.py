#encoding=utf-8

# importregstab.py
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

This module provides a controller class which coordinates the import of
registrations. The main window class acts as some bridge here as this is the
class which receives all events on the tab page and which delegates them over
here.
'''

# Public export of module content
__all__ = [
    "ImportRegsTab"
]


# Class definition
class ImportRegsTab:
    '''
    This delegate class coordinates the import of registrations.
    '''

    def __init__(self, wndMain):
        '''
        Constructor. Takes a MainWindow instance as parameter because as
        coordinating controller class access to the UI is needed.
        '''
        pass


    def openBankFile(self):
        '''
        Delegate method called by the UI. Asks the user for a bank file to
        open, reads the file contents and populates the import list.
        '''
        print "open bank file"
        pass


    def importSelectedRegs(self):
        '''
        Delegate method called by the UI. Imports the selected registrations
        from the import list. Each registration will be stored in its own
        file in the working directory.
        '''
        print "import selected regs"
        pass
