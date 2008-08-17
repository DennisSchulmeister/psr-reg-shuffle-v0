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


# Import global modules
import kiwi.ui.dialogs
import os.path
import gtk

# Import application modules
import regbank.bankfile
import regfile.regfile
import mainwindow
import main
import util
import const


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
        # Initialize attributes
        self.main    = main.Main.getInstance()
        self.wndMain = wndMain
        self.regList = []

        # Add images to buttons
        img = gtk.Image()
        img.set_from_stock(gtk.STOCK_OPEN, gtk.ICON_SIZE_BUTTON)
        self.wndMain.btnOpenBankFile.set_property("image_position", gtk.POS_TOP)
        self.wndMain.btnOpenBankFile.set_image(img)

        img = gtk.Image()
        img.set_from_stock(gtk.STOCK_APPLY, gtk.ICON_SIZE_BUTTON)
        self.wndMain.btnImportSelectedRegs.set_property("image_position", gtk.POS_TOP)
        self.wndMain.btnImportSelectedRegs.set_image(img)

        img = gtk.Image()
        img.set_from_stock(gtk.STOCK_CLEAR, gtk.ICON_SIZE_BUTTON)
        self.wndMain.btnImportClear.set_property("image_position", gtk.POS_TOP)
        self.wndMain.btnImportClear.set_image(img)

        # Assume empty list
        self.wndMain.oblImportRegs.clear()
        self.onListEmptyChanged(self.wndMain.oblImportRegs, False)


    def openBankFile(self):
        '''
        Delegate method called by the UI. Asks the user for a bank file to
        open, reads the file contents and populates the import list.
        '''
        # Open bank file given by user
        filename = kiwi.ui.dialogs.open(
            title    = _("Open bank file"),
            parent   = self.wndMain.wndMain,
            patterns = ["*.REG", "*.reg", "*.RGT", "*.rgt"]
        )

        if not filename:
            return

        # Change processe's working directory so that file dialogs remember it
        self.main.chdirFromFilename(
            filename = filename
        )

        # Search suitable RegBank class
        regBankClass = regbank.bankfile.BankFile.getClassForBankFile(filename=filename)
        regBankObj   = regBankClass(filename=filename)
        keyModel     = regBankObj.getKeyboardName()

        # Retrieve registrations and populate import list
        self.regList = regBankObj.getRegistrationObjects()
        self.wndMain.oblImportRegs.clear()

        i = 0
        for regObj in self.regList:
            i += 1

            if regObj:
                regName = regObj.getName()
                mark    = True
            else:
                regName = _("### EMPTY ###")
                mark    = False

            entry = mainwindow.ImportRegsEntry(
                mark   = mark,
                pos    = i,
                name   = regName,
                model  = keyModel,
                regObj = regObj
            )

            self.wndMain.oblImportRegs.append(entry)

        # Show success message
        self.wndMain.setStatusMessage(const.msg["bank-open-success"] % {
                "filename": filename,
            }
        )


    def importSelectedRegs(self):
        '''
        Delegate method called by the UI. Imports the selected registrations
        from the import list. Each registration will be stored in its own
        file in the working directory.
        '''
        # Store each selected registration to its own file
        count = 0

        for regEntry in self.wndMain.oblImportRegs:
            # Skip entry if not marked for import or if empty
            if not regEntry.mark or not regEntry.regObj:
                continue

            # Count imported registrations
            count += 1

            # Rename registration
            regEntry.regObj.setName(regEntry.name)

            # Create registration file in memory
            regFile = regfile.regfile.RegFile()
            regFile.setKeyboardName(regEntry.model)
            regFile.setRegistrationObject(regEntry.regObj)

            # Calculate file name
            fileName = util.calculateFileNameFromRegName(regEntry.name, self.main.workDir)

            # Store file
            regFile.storeRegFile(fileName)

        # Break if no registration could be imported
        if not count:
            self.wndMain.setStatusMessage(const.msg["nothing-imported"])
            return

        # Update list of available registrations
        self.wndMain.updateAvailableRegList()

        # Show success message
        self.wndMain.setStatusMessage(const.msg["import-ok"] % (count))


    def clearList(self):
        '''
        Delegate method called by the UI. Clears the import list.
        '''
        self.wndMain.oblImportRegs.clear()


    def onListEmptyChanged(self, list, hasRows):
        '''
        Delegate method called by the UI whenever the list of registrations
        to be imported changes its empty state. Used to disable or enable
        buttons.
        '''
        self.wndMain.btnImportSelectedRegs.set_sensitive(hasRows)
        self.wndMain.btnImportClear.set_sensitive(hasRows)
