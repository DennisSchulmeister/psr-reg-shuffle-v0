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

This module provides a class for exporting the content a setlist to a
plain text file.
'''

# Public export of module content
__all__ = [
    "ExportText",
]


# Import global modules
import kiwi.ui.dialogs

# Import application modules
import appexceptions
import exportbase
from .. import const


# Class for text file export
class ExportText(exportbase.ExportBase):
    '''
    This class allows to export the contents of a list of BankFiles to
    plain text files.
    '''

    # Static attributes........................................................

    displayName = _("Export Plain _Text")


    # Export routines..........................................................

    def getSuccessMessage(self):
        '''
        Returns a success message which can be shown after successful export.
        '''
        return const.msg["setlist-export-ok"] % (self.filename)


    def prepare(self):
        '''
        Called before the export begins. Can be used to ask user for filename
        etc. Needs to throw appexceptions.Cancel if the user chooses to abort.
        '''
        # Ask user for filename
        self.filename = kiwi.ui.dialogs.save(
            title        = _("Save text file"),
            parent       = self.wndMain.wndMain,
            current_name = "*.txt"
        )

        if self.filename:
            # Change processe's working directory for file dialogs
            self.main.chdirFromFilename(
                filename = self.filename
            )

            # Create file
            self.fileObj = open(self.filename, "w")

            # Print setlist name
            self.fileObj.write("%s\n" % (self.printName))
        else:
            raise appexceptions.Cancel()


    def onNewBank(self, setlistEntry):
        '''
        Called each time a new bank starts. Used to export the bank's name.
        Takes a printsetlisttab.SetlistEntry object.
        '''
        # Get bank name
        bankName = setlistEntry.shortname

        # Print spacing and bank name
        self.fileObj.write("\n%s\n" % (bankName))

        # Reset registration counter
        self.regCount = 0


    def onNewRegistration(self, regObj):
        '''
        Called for each registration within a bank. Used to export the
        registration's data. Takes Registration object.
        '''
        if regObj:
            regName = regObj.stripName(regObj.getName())
        else:
            regName = const.REG_NAME_EMPTY

        self.regCount += 1
        regNr = "[%i]" % (self.regCount)

        self.fileObj.write("%s %s\n" % (regNr, regName))


    def finish(self):
        '''
        Called after exporting all bank files. Used to close files, start
        printing etc.
        '''
        # Export trailing newline
        self.fileObj.write("\n")

        # Close export file
        if self.fileObj:
            self.fileObj.close()
