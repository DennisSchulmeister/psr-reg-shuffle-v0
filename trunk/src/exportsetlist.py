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

This module provides classes for exporting (and printing) the contents of
bank files given as a list of BankFile objects.
'''

# Public export of module content
__all__ = [
    "ExportSetlistBase",
    "ExportSetlistText",
    "ExportSetlistCSV",
    "ExportSetlistPrint",
]


# Import global modules
import kiwi.ui.dialogs

# Import application modules
import appexceptions
import main
import const


# Base class for all export types
class ExportSetlistBase:
    '''
    Base class for the export of BankFile contents.
    '''

    # Constructor..............................................................

    def __init__(self, wndMain=None, name="", setlistEntries=[]):
        '''
        Constructor. Takes a sequence of printsetlisttab.SetlistEntry objects.
        '''
        # Parameter check
        if not name:
            name = _("Setlist")

        # Store values
        self.main = main.Main.getInstance()
        self.wndMain = wndMain
        self.name = name
        self.setlistEntries = setlistEntries


    # Public API...............................................................

    def getClassByExportType(cls, format=""):
        '''
        A static method which determines the class object whose instances can
        be used to export a BankFile list to the fiven format.

        Format can be:

        * const.EXPORT_PRINT
        * const.EXPORT_TEXT
        * const.EXPORT_CSV

        Otherwise appexceptions.InvalidExportFormat is raised.
        '''
        if format == const.EXPORT_PRINT:
            return ExportSetlistText

        elif format == const.EXPORT_TEXT:
            return ExportSetlistText

        elif format == const.EXPORT_CSV:
            return ExportSetlistCSV

        else:
            raise appexceptions.InvalidExportFormat(format)

    getClassByExportType = classmethod(getClassByExportType)


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


# Class for text file export
class ExportSetlistText(ExportSetlistBase):
    '''
    This class allows to export the contents of a list of BankFiles to
    plain text files.
    '''

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
            title        = _("Save Text File"),
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
            self.fileObj.write("%s\n" % (self.name))
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
        # Close export file
        if self.fileObj:
            self.fileObj.close()


# Class for CSV export
class ExportSetlistCSV(ExportSetlistBase):
    '''
    This class allows to export the contents of a list of BankFiles to
    CSV files.
    '''

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
            title        = _("Save CSV File"),
            parent       = self.wndMain.wndMain,
            current_name = "*.csv"
        )

        if self.filename:
            # Change processe's working directory for file dialogs
            self.main.chdirFromFilename(
                filename = self.filename
            )

            # Create file
            self.fileObj = open(self.filename, "w")

            # Print setlist name
            self.fileObj.write("\"%s\"\n" % (self.name))
        else:
            raise appexceptions.Cancel()


    def onNewBank(self, setlistEntry):
        '''
        Called each time a new bank starts. Used to export the bank's name.
        Takes a printsetlisttab.SetlistEntry object.
        '''
        # Get bank name
        bankName = setlistEntry.shortname
        bankName = bankName.replace("\t", " ")

        # Print spacing and bank name
        self.fileObj.write("\n\"%s\"\n" % (bankName))

        # Reset registration counter
        self.regCount = 0


    def onNewRegistration(self, regObj):
        '''
        Called for each registration within a bank. Used to export the
        registration's data. Takes Registration object.
        '''
        # Print registration number and name
        if regObj:
            regName = regObj.stripName(regObj.getName())
            regName = regName.replace("\t", " ")
        else:
            regName = const.REG_NAME_EMPTY

        self.regCount += 1

        self.fileObj.write("%i\t\"%s\"\n" % (self.regCount, regName))


    def finish(self):
        '''
        Called after exporting all bank files. Used to close files, start
        printing etc.
        '''
        # Close export file
        if self.fileObj:
            self.fileObj.close()


# Class for setlist printing
class ExportSetlistPrint(ExportSetlistBase):
    '''
    This class allows to print the contents of a list of BankFiles.
    '''

    # Export routines..........................................................

    def getSuccessMessage(self):
        '''
        Returns a success message which can be shown after successful export.
        '''
        return const.msg["setlist-print-ok"]


    def prepare(self):
        '''
        Called before the export begins. Can be used to ask user for filename
        etc. Needs to throw appexceptions.Cancel if the user chooses to abort.
        '''
        # Nothing to do. Print dialog can only be shown on finish.
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
