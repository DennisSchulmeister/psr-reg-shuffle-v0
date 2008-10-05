#encoding=utf-8

# exportsetlisttab.py
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

This module provides the base class for all exporters.
'''

# Public export of module content
__all__ = [
    "ExportBase",
]


# Import global modules
## NONE YET

# Import application modules
from .. import util


# Base class for all export types
class ExportBase:
    '''
    Base class for the export of BankFile contents.
    '''

    # Static attributes........................................................

    displayName = ""          # Name shown on the UI


    # Constructor..............................................................

    def __init__(self, wndMain=None, printName="", setlistEntries=[]):
        '''
        Constructor. Takes a sequence of printsetlisttab.SetlistEntry objects.
        '''
        # Parameter check
        if not printName:
            printName = _("Setlist")

        # Store values
        ##self.main = main.Main.getInstance()
        self.main = util.getMainInstance()
        self.wndMain = wndMain
        self.printName = printName
        self.setlistEntries = setlistEntries


    # Public API...............................................................

    def getExporterClasses(cls):
        '''
        This method returns a flat list of class objects which are all
        sub-classes of ExportBase.
        '''
        classes = []

        for candidate in __EXPORT_CLASSES__:
            if not candidate == ExportBase \
            and issubclass(candidate, ExportBase):
                classes.append(candidate)

        return classes

    getExporterClasses = classmethod(getExporterClasses)


    def do(self):
        '''
        Base method used to trigger the export process. This is the only method
        a user should call. Throws appexceptions.Cancel if the user aborts.
        Returns string with success message otherwise.
        '''
        # Ask for filename etc. (Might raise appexceptions.Cancel)
        self.prepare()

        # Export registration banks
        for setlistEntry in self.setlistEntries:
            self.onNewBank(setlistEntry)

            for regObj in setlistEntry.bankObj.getRegistrationObjects():
                self.onNewRegistration(regObj)

        # Finish operation
        self.finish()

        # Return success message
        return self.getSuccessMessage()


    # Methods to be overwritten................................................

    def getSuccessMessage(self):
        '''
        Returns a success message which can be shown after successful export.
        '''
        return ""


    def prepare(self):
        '''
        Called before the export begins. Can be used to ask user for filename
        etc. Needs to throw appexceptions.Cancel if the user chooses to abort.
        '''
        pass


    def onNewBank(self, setlistEntry):
        '''
        Called each time a new bank starts. Used to export the bank's name.
        Takes a printsetlisttab.SetlistEntry object.
        '''
        pass


    def onNewRegistration(self, regObj):
        '''
        Called for each registration within a bank. Used to export the
        registration's data. Takes Registration object.
        '''
        pass


    def finish(self):
        '''
        Called after exporting all bank files. Used to close files, start
        printing etc.
        '''
        pass
