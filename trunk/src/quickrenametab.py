#encoding=utf-8

# quickrenametab.py
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

This module provides a controller class which allows to rename all
regsitrations of a bank file without importing them first. The main window
class acts as some bridge here as this is the class which receives all events
on the tab page and which delegates them over here.
'''

# Public export of module content
__all__ = [
    "QuickRenameTab"
]


# Import global modules
import kiwi.ui.dialogs
import os.path
import gtk
import gtk.gdk
import gobject

from kiwi.ui.objectlist    import ObjectList
from kiwi.ui.objectlist    import Column

# Import application modules
import regbank.bankfile
import regfile.regfile
import mainwindow
import main
import util
import const


# Class definition
class QuickRenameTab(gobject.GObject):
    '''
    This delegate class allows to rename registrations of a bank file
    without importing them first.

    Emited signals:
    ---------------

    *rename-list-updated*: Emited after the bank file list has changed.
    '''

    def __init__(self, wndMain):
        '''
        Constructor. Takes a MainWindow instance as parameter because as
        coordinating controller class access to the UI is needed.
        '''
        # Initialize attributes
        self.main    = main.Main.getInstance()
        self.wndMain = wndMain

         # Define signals
        gobject.GObject.__init__(self)

        gobject.signal_new(
            "rename-list-updated",
            QuickRenameTab,
            gobject.SIGNAL_RUN_LAST,
            gobject.TYPE_NONE,
            (gobject.TYPE_PYOBJECT,),
        )

        # Build list of known file extensions
        self.allExtensions = []

        for ext in regbank.bankfile.BankFile.getAllFileExtensions():
            extLow = "*.%s" % (ext.lower())
            extUp  = "*.%s" % (ext.upper())

            if not extLow in self.allExtensions:
                self.allExtensions.append(extLow)

            if not extUp in self.allExtensions:
                self.allExtensions.append(extUp)

        # Insert ObjectList into main window
        self.oblRenameRegs = ObjectList(
            [
                Column("pos",  title=_("Number"), editable=False),
                Column("name", title=_("Registration Name"), editable=True, searchable=True, expand=True),
            ]
        )

        self.wndMain.evtRenameRegs.add(self.oblRenameRegs)
        self.oblRenameRegs.show()

        self.oblRenameRegs.connect("has-rows", self.onListEmptyChanged)
        self.oblRenameRegs.connect("cell-edited", self.on_oblRenameRegs_cell_edited)
        self.connect("rename-list-updated", self.onListUpdated)

        # Add images to buttons
        img = gtk.Image()
        img.set_from_stock(gtk.STOCK_OPEN, gtk.ICON_SIZE_BUTTON)
        self.wndMain.btnRenameOpen.set_property("image_position", gtk.POS_TOP)
        self.wndMain.btnRenameOpen.set_image(img)

        img = gtk.Image()
        img.set_from_stock(gtk.STOCK_SAVE, gtk.ICON_SIZE_BUTTON)
        self.wndMain.btnRenameSave.set_property("image_position", gtk.POS_TOP)
        self.wndMain.btnRenameSave.set_image(img)

        img = gtk.Image()
        img.set_from_stock(gtk.STOCK_CLEAR, gtk.ICON_SIZE_BUTTON)
        self.wndMain.btnRenameClear.set_property("image_position", gtk.POS_TOP)
        self.wndMain.btnRenameClear.set_image(img)

        # Assume empty list
        self.oblRenameRegs.clear()
        self.filename   = ""
        self.regBankObj = None

        self.onListEmptyChanged(self.oblRenameRegs, False)


    # Bankfile access..........................................................

    def openBankFile(self):
        '''
        Delegate method called by the UI. Asks the user for a bank file to
        open, reads the file contents and populates the import list.
        '''
        # Open bank file given by user
        filename = kiwi.ui.dialogs.open(
            title    = _("Open bank file"),
            parent   = self.wndMain.wndMain,
            patterns = self.allExtensions
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

        # Remember filename and BankFile object
        self.filename   = filename
        self.regBankObj = regBankObj


        # Retrieve registrations and populate list
        regList = regBankObj.getRegistrationObjects()
        self.oblRenameRegs.clear()

        i = 0
        for regObj in regList:
            i += 1

            if regObj:
                regName = regObj.getName()
                mark    = True
            else:
                regName = const.REG_NAME_EMPTY

            entry = RenameRegsEntry(
                pos    = i,
                name   = regName,
                model  = keyModel,
                regObj = regObj
            )

            self.oblRenameRegs.append(entry)

        # Emit rename-list-updated signal
        self.emit("rename-list-updated", self.oblRenameRegs)

        # Show success message
        self.wndMain.setStatusMessage(const.msg["bank-open-success"] % {
                "filename": filename,
            }
        )


    def saveBankFile(self):
        '''
        Delegate method called by teh UI. Saves the changed registration
        bank file again.
        '''
        # Make sure a BankFile object exists
        if not self.regBankObj:
            return

        # Assemble list of registration objects and rename registrations
        regList = []

        for regEntry in self.oblRenameRegs:
            regObj = None

            if regEntry.regObj:
                regObj = regEntry.regObj
                regObj.setName(regEntry.name)

            regList.append(regObj)

        # Save bank file
        self.regBankObj.setRegistrationObjects(regList)
        self.regBankObj.storeBankFile(self.filename)

        # Show success message
        self.wndMain.setStatusMessage(const.msg["bank-save-ok"] % (self.filename))


    # List content management..................................................

    def moveSelectedUp(self):
        '''
        Delegate method called by the UI. Moves the selected entry up by
        one position.
        '''
        # Move selected entry up
        pos = self.oblRenameRegs.get_selected_row_number()

        if not pos or pos < 1:
            return

        row = self.oblRenameRegs.get_selected()
        self.oblRenameRegs.remove(row)

        self.oblRenameRegs.insert(
            index    = pos - 1,
            instance = row,
            select   = True
        )

        # Give short success message
        self.wndMain.setStatusMessage(const.msg["moved-one-up"] % (row.name))


    def moveSelectedDown(self):
        '''
        Delegate method called by the UI. Moves the selected entry down by
        one position.
        '''
        # Move selected entry down
        pos = self.oblRenameRegs.get_selected_row_number()

        if pos < 0 or pos >= len(self.oblRenameRegs) - 1:
            return

        row = self.oblRenameRegs.get_selected()
        self.oblRenameRegs.remove(row)

        self.oblRenameRegs.insert(
            index    = pos + 1,
            instance = row,
            select   = True
        )

        # Give short success message
        self.wndMain.setStatusMessage(const.msg["moved-one-down"] % (row.name))


    def clearList(self):
        '''
        Delegate method called by the UI. Clears the import list.
        '''
        # Clear list content
        self.oblRenameRegs.clear()

        # Close bank file
        self.regBankObj = None
        self.filename   = ""


    # Widget event handlers....................................................

    def onListEmptyChanged(self, list, hasRows):
        '''
        Delegate method called by the UI whenever the list of registrations
        to be imported changes its empty state. Used to disable or enable
        buttons.
        '''
        # Enable or disable buttons
        self.wndMain.btnRenameSave.set_sensitive(hasRows)
        self.wndMain.btnRenameClear.set_sensitive(hasRows)

        # Set list heading
        if not hasRows:
            heading = _("No open file")
        else:
            filename = os.path.split(self.filename)[1]
            heading  = _("Content of %s") % (filename)

        self.wndMain.lblRenameRegs.set_text(heading)

        # Emit rename-list-updated signal
        self.emit("rename-list-updated", list)


    def onListUpdated(self, tab, *list):
        '''
        Event handler which responds to the list being updated. Used to control
        move up and down buttons.
        '''
        moreThanOne = len(list[0]) > 1
        self.wndMain.btnRenameUp.set_sensitive(moreThanOne)
        self.wndMain.btnRenameDown.set_sensitive(moreThanOne)


    def on_oblRenameRegs_cell_edited(self, *args):         # Manually connected
        '''
        Event handler which responds whenever the user edits the name of
        a registration. Makes sure that no ### EMPTY ### entry can be
        renamed.
        '''
        # Don't allow editing of dummy registrations (### EMPTY ###)
        regEntry = args[1]

        if not regEntry.regObj:
            regEntry.name = const.REG_NAME_EMPTY
            return


# Class definition of list entries
class RenameRegsEntry:
    '''
    List entry class for the "Quick Rename" list. Holds the following
    values which can all be accessed from the list.

    * pos,   Position in registration bank
    * name,  Name of registration
    * model, Internal name of the keyboard model
    * reg,   Registration Object
    '''

    def __init__(self, pos=0, name="", model="", regObj=None):
        '''
        Constructor. Just stores the given parameters.
        '''
        self.pos    = pos
        self.name   = name
        self.model  = model
        self.regObj = regObj
