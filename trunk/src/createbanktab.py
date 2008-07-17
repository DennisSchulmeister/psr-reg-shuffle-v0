#encoding=utf-8

# createbanktab.py
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

This module provides a controller class which coordinates the creation of
registration banks. The main window class acts as some bridge here as this
is the class which receives all events on the tab page and which delegates
them over here.
'''

# Public export of module content
__all__ = [
    "CreateBankTab"
]


# Class definition
class CreateBankTab:
    '''
    This delegate class coordinates the assembly of bank files.
    '''

    def __init__(self, wndMain):
        '''
        Constructor. Takes a MainWindow instance as parameter because as
        coordinating controller class access to the UI is needed.
        '''
        pass


    def on_main__work_dir_changed(self, workDir):
        '''
        Event handler for changed working directory. Updates the list of
        available registrations.
        '''
        pass


    def removeSelectedItemsFromExportList(self):
        '''
        Delegate method called by the UI. Removes all selected items from the
        export list.
        '''
        print "remove selected"
        pass


    def removeAllItemsFromExportList(self):
        '''
        Delegate method called by the UI. Removes all items from the export
        list.
        '''
        print "remove all"
        pass


    def saveBankFile(self):
        '''
        Delegate method called by the UI. Asks the user for a filename and
        stores all registrations from the export list in it.
        '''
        print "save bank file"
        pass
