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

# Import global modules
import os
import os.path
import glob
import gtk.gdk
import gobject
import kiwi.ui.dialogs

# Import application modules
import appexceptions
import regfile
import mainwindow
import batchdialog
import const
import main
import easydraganddrop
import regbank
import util

# Class definition
class CreateBankTab(gobject.GObject):
    '''
    This delegate class coordinates the assembly of bank files.

    Emited signals:
    ---------------

    *reglist-updated*: Emited after the list of available registrations
    has changed. (Without renames)

    *newlist-updated*: Emited after the export list has changed. (Without
    renames)
    '''

    # Object creation..........................................................

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
            "reglist-updated",
            CreateBankTab,
            gobject.SIGNAL_RUN_LAST,
            gobject.TYPE_NONE,
            (),
        )

        gobject.signal_new(
            "newlist-updated",
            CreateBankTab,
            gobject.SIGNAL_RUN_LAST,
            gobject.TYPE_NONE,
            (),
        )

        # Connect to main.work_dir_changed signal
        self.main.connect("work-dir-changed", self.on_main__work_dir_changed)

        # Connect to drag and drop signals
        # NOTE: Source is always the encapsulated TreeView but destination
        # is the ObjectList which holds the TreeView!
        self.dndAvailableRegs = easydraganddrop.EasyDragAndDrop(
            srcWidget  = self.wndMain.oblNewBank.get_treeview(),
            dstWidget  = self.wndMain.oblAvailableRegs,
            checkFunc  = lambda row: True,
            actionFunc = lambda src, dst, row: self.removeColumn(
                src = src,
                dst = dst,
                row = row
            ),
            dataFunc   = lambda: self.getDataNewBank()
        )

        self.dndNewBank = easydraganddrop.EasyDragAndDrop(
            srcWidget  = self.wndMain.oblAvailableRegs.get_treeview(),
            dstWidget  = self.wndMain.oblNewBank,
            checkFunc  = lambda row: self.checkCopyRegToNewBank(row),
            actionFunc = lambda src, dst, row: self.copyColumn(
                src = src,
                dst = dst,
                row = row
            ),
            dataFunc   = lambda: self.getDataAvailableRegs()
        )

        # Pre-fill filter combobx
        self.wndMain.cbxNewBankAvailFilter.clear()
        self.wndMain.cbxNewBankAvailFilter.append_item(_("Show All"),        "ALL")
        self.wndMain.cbxNewBankAvailFilter.append_item(_("Compatible Only"), "COMPATIBLE")
        self.wndMain.cbxNewBankAvailFilter.append_item(_("Selected Model"),  "MODEL")

        self.wndMain.cbxNewBankAvailFilter.select("ALL")
        self.wndMain.cbxNewBankAvailFilter.update("ALL")

        # Pre-fill keyboard model combobox
        self.wndMain.cbxNewBankKeyModel.clear()
        self.wndMain.cbxNewBankKeyModel.append_item(const.keyboardNameLong[const.UNKNOWN_MODEL], const.UNKNOWN_MODEL)

        try:
            models  = []
            classes = regbank.bankfile.BankFile.getAllSubclasses()

            for cls in classes:
                for model in cls.keyboardNames:
                    if not model in models:
                        models.append(model)

            models.sort()

            for model in models:
                if model == const.ALL_MODELS \
                or model == const.UNKNOWN_MODEL:
                    continue

                label = const.keyboardNameLong[model]
                self.wndMain.cbxNewBankKeyModel.append_item(label, model)
        except appexceptions.NoClassFound:
            pass

        self.wndMain.cbxNewBankKeyModel.select(const.UNKNOWN_MODEL)
        self.wndMain.cbxNewBankKeyModel.update(const.UNKNOWN_MODEL)

        self.allowedKeyboardNames = []


        # Add images to buttons
        img = gtk.Image()
        img.set_from_stock(gtk.STOCK_GO_FORWARD, gtk.ICON_SIZE_BUTTON)
        self.wndMain.btnAddSelected.set_property("image_position", gtk.POS_TOP)
        self.wndMain.btnAddSelected.set_image(img)

        img = gtk.Image()
        img.set_from_stock(gtk.STOCK_GO_BACK, gtk.ICON_SIZE_BUTTON)
        self.wndMain.btnRemoveSelected.set_property("image_position", gtk.POS_TOP)
        self.wndMain.btnRemoveSelected.set_image(img)

        img = gtk.Image()
        img.set_from_stock(gtk.STOCK_EXECUTE, gtk.ICON_SIZE_BUTTON)
        self.wndMain.btnBatch.set_property("image_position", gtk.POS_TOP)
        self.wndMain.btnBatch.set_image(img)

        img = gtk.Image()
        img.set_from_stock(gtk.STOCK_CLEAR, gtk.ICON_SIZE_BUTTON)
        self.wndMain.btnClearList.set_property("image_position", gtk.POS_TOP)
        self.wndMain.btnClearList.set_image(img)

        img = gtk.Image()
        img.set_from_stock(gtk.STOCK_SAVE_AS, gtk.ICON_SIZE_BUTTON)
        self.wndMain.btnSaveBank.set_property("image_position", gtk.POS_TOP)
        self.wndMain.btnSaveBank.set_image(img)

        # Events for checking allowed buttons
        self.connect("reglist-updated", self.checkAllowedButtons)
        self.connect("newlist-updated", self.checkAllowedButtons)
        self.wndMain.cbxNewBankKeyModel.connect("content-changed", self.checkAllowedButtons)


    # Work directory access ...................................................

    def on_main__work_dir_changed(self, obj, workDir):
        '''
        Event handler for changed working directory. Updates the list of
        available registrations.
        '''
        # Remove all items from list
        self.wndMain.oblAvailableRegs.clear()

        # Retrieve list of available files
        pattern   = os.path.join(workDir, "*.%s" % (regfile.extension))
        filenames = glob.glob(pattern)

        # Append empty registration entry to list
        entry = mainwindow.AvailableRegsEntry(
            name     = _("### EMPTY ###"),
            keyName  = const.keyboardNameLong[const.ALL_MODELS],
            model    = const.ALL_MODELS,
            fileName = ""
        )

        self.wndMain.oblAvailableRegs.append(entry)

        # Read files and append to list
        for filename in filenames:
            # Skip bad files
            if not regfile.regfile.RegFile.canUnderstandFile(filename=filename):
                continue

            # Read registration data and populate list
            regFile = regfile.regfile.RegFile(filename=filename)

            entry = mainwindow.AvailableRegsEntry(
                name     = regFile.getRegistrationObject().getName(),
                keyName  = const.keyboardNameLong[regFile.getKeyboardName()],
                model    = regFile.getKeyboardName(),
                fileName = filename
            )

            self.wndMain.oblAvailableRegs.append(entry)

        # Emit reglist-updated signal
        self.emit("reglist-updated")


    def availableRegRename(self, regEntry):
        '''
        Delegate method called by UI. Responds to a renamed available
        registration by changing the registration file's content and name.
        '''
        # Dont process dummy registrtions (### EMPTY ###)
        if not regEntry.fileName:
            return

        # Access registration binary data
        regFile = regfile.regfile.RegFile(filename=regEntry.fileName)
        regObj  = regFile.getRegistrationObject()

        # Abort if name didn't change
        if regEntry.name == regObj.getName():
            return

        # Store changed name into binary data
        oldName = regObj.getName()
        regObj.setName(regEntry.name)

        # Save registration file with new file name (but keep old file)
        oldFileName = regEntry.fileName
        newFileName = util.calculateFileNameFromRegName(regEntry.name, self.main.workDir)
        regFile.storeRegFile(newFileName)

        # Change entry of available registration list in-place (no list reload)
        regEntry.fileName = newFileName

        # Scan list of new bank file and replace old filename if found
        for newReg in self.wndMain.oblNewBank:
            # Skip dummy registrations
            if not newReg.fileName:
                continue

            # Skip files whose file name doesn't match anyway
            if not os.path.samefile(newReg.fileName, oldFileName):
                continue

            # Change file name
            newReg.fileName = newFileName

            # Change name if it matches old name
            if newReg.name == oldName:
                newReg.name = regEntry.name

            # Update displayed list
            self.wndMain.oblNewBank.update(newReg)

        # Delete old file with old name
        if not os.path.samefile(oldFileName, newFileName):
            os.unlink(oldFileName)

        # Emit reglist-updated signal
        self.emit("reglist-updated")


    # List of available registrations .........................................

    def doBatch(self):
        '''
        Delegate method called by the UI. Gets called when the user activates
        the "Batch" button. Uses a BatchDialog object in order to show a
        modal dialog which performs the processing.
        '''
        # Make sure a valid keyboard model was selected
        keyboardName = self.getNewBankKeyboardName()

        if keyboardName == const.ALL_MODELS \
        or keyboardName == const.UNKNOWN_MODEL:
            self.wndMain.setStatusMessage(const.msg["invalid-key-name"])
            return

        # Collect registrations for the dialog
        regEntryList = []

        for entry in self.wndMain.oblAvailableRegs:
            if not entry.fileName:
                continue

            regEntryList.append(entry)

        batchDialog = batchdialog.BatchDialog(keyboardName, regEntryList)
        batchDialog.show()
        batchDialog.destroy()


########## TODO: Filter ####################

    # Export list of new bank file ............................................

    def onNewBankEmptyChanged(self, list, hasRows):
        '''
        Delegate methode called by the UI. Gets called whenever the list of
        a new bank becomes empty or non-empty. This is cruical for activating
        and deactivating the keyboard model combobox.
        '''
        # Disable keyboard selection when export list is not empty
        self.wndMain.cbxNewBankKeyModel.set_sensitive(not hasRows)

        # Emit newlist-changed signal
        self.emit("newlist-updated")


    def addSelectedItemsToExport(self):
        '''
        Delegate method called by the UI. Copies the selected items from the
        available list to the export list.
        '''
        # Get selected row
        row = self.wndMain.oblAvailableRegs.get_selected()

        if not row:
            return


        # Check whether copying is allowed (just like DnD would do)
        if not self.checkCopyRegToNewBank(row):
            return

        # Copy row to export list
        self.copyColumn(self.wndMain.oblAvailableRegs, self.wndMain.oblNewBank, row)

        # Emit newlist-changed signal
        self.emit("newlist-updated")


    def removeSelectedItemsFromExportList(self):
        '''
        Delegate method called by the UI. Removes all selected items from the
        export list.
        '''
        #for entry in self.wndMain.oblNewBank.get_selected_rows():
        #    self.wndMain.oblNewBank.remove(entry)
        self.removeColumn(None, None, self.wndMain.oblNewBank.get_selected())

        # Emit newlist-changed signal
        self.emit("newlist-updated")


    def removeAllItemsFromExportList(self):
        '''
        Delegate method called by the UI. Removes all items from the export
        list.
        '''
        self.wndMain.oblNewBank.clear()
        self.wndMain.setStatusMessage(const.msg["clear-ok"])


    def newBankMoveSelectedUp(self):
        '''
        Delegate method called by the UI. Moves the selected registration
        of a new bank file down by one position.
        '''
        # Move selected entry up
        pos = self.wndMain.oblNewBank.get_selected_row_number()

        if not pos or pos < 1:
            return

        row = self.wndMain.oblNewBank.get_selected()
        self.wndMain.oblNewBank.remove(row)

        self.wndMain.oblNewBank.insert(
            index    = pos - 1,
            instance = row,
            select   = True
        )

        # Give short success message
        self.wndMain.setStatusMessage(const.msg["moved-one-up"] % (row.name))


    def newBankMoveSelectedDown(self):
        '''
        Delegate method called by the UI. Moves the selected registration
        of a new bank file up by one position.
        '''
        # Move selected entry down
        pos = self.wndMain.oblNewBank.get_selected_row_number()

        if pos < 0 or pos >= len(self.wndMain.oblNewBank) - 1:
            return

        row = self.wndMain.oblNewBank.get_selected()
        self.wndMain.oblNewBank.remove(row)

        self.wndMain.oblNewBank.insert(
            index    = pos + 1,
            instance = row,
            select   = True
        )

        # Give short success message
        self.wndMain.setStatusMessage(const.msg["moved-one-down"] % (row.name))


    def saveBankFile(self):
        '''
        Delegate method called by the UI. Asks the user for a filename and
        stores all registrations from the export list in it.
        '''
        # Check for valid keyboard model
        if self.getNewBankKeyboardName() == const.UNKNOWN_MODEL \
        or self.getNewBankKeyboardName() == const.ALL_MODELS:
            self.wndMain.setStatusMessage(const.msg["invalid-key-name"])
            return

        model = self.getNewBankKeyboardName()
        bankClass = regbank.bankfile.BankFile.getClassForKeyboardName(model)

        # Ask user for file name
        fileName = kiwi.ui.dialogs.save(
            title        = _("Save Registration Bank"),
            parent       = self.wndMain.wndMain,
            current_name = "*.%s" % (bankClass.fileExt)
        )

        if not fileName:
            return

        # Change processe's working directory so that file dialogs remember it
        self.main.chdirFromFilename(
            filename = fileName
        )

        # Read binary registration data from disk
        # And assemble list of Registration objects.
        # While at it also apply name changes.
        regList = []

        for regEntry in self.wndMain.oblNewBank:
            regFile = regfile.regfile.RegFile(filename=regEntry.fileName)
            regObj  = regFile.getRegistrationObject()

            if regObj:
                regObj.setName(regEntry.name)

            regList.append(regObj)

        # Append empty registrations as necessary
        missing = bankClass.maxReg - len(regList)

        if missing > 0:
            for i in range(missing):
                regList.append(None)

        # Create new bank file object
        bankFile = bankClass(keyboardName=model)
        bankFile.setRegistrationObjects(regList)

        # Store file to disk
        bankFile.storeBankFile(fileName)

        # Show success message
        self.wndMain.setStatusMessage(const.msg["bank-save-ok"] % (fileName))


    def getNewBankKeyboardName(self):
        '''
        Determines the technical keyboard name (model) for which the new
        registration bank shall be created. As of version 0.2 this is just
        the model selected in the keyboard model combobox.
        '''
        # Retrieve selected keyboard model
        return self.wndMain.cbxNewBankKeyModel.get_selected_data()


    def onKeyboardModelChanged(self, widget):
        '''
        Delegate methode called by the UI whenever the user selects another
        keyboard model from the combobox.
        '''
        # Retrieve list of allowed keyboard models (for mix-in)
        keyName = self.getNewBankKeyboardName()

        if keyName == const.UNKNOWN_MODEL \
        or keyName == const.ALL_MODELS:
            self.allowedKeyboardNames = []
            return

        regClass = regbank.bankfile.BankFile.getClassForKeyboardName(keyboardName=keyName)
        self.allowedKeyboardNames = regClass.getAllKeyboardNames()


    # Drag and drop support....................................................

    def checkCopyRegToNewBank(self, row):
        '''
        This method gets called by an EasyDragAndDrop object which implements
        the drag and drop behaviour for both TreeViews.
        '''
        # Check keyboard model
        newBankModel = self.getNewBankKeyboardName()
        RegModel     = row.model

        if newBankModel == const.UNKNOWN_MODEL:
            self.wndMain.setStatusMessage(const.msg["invalid-key-name"])
            return False

        elif not RegModel     in self.allowedKeyboardNames \
        and  not RegModel     == const.ALL_MODELS          \
        and  not newBankModel == const.ALL_MODELS:
            self.wndMain.setStatusMessage(
                const.msg["incompatible-keys"] % {
                    "srcName": const.keyboardNameLong[RegModel],
                    "dstName": const.keyboardNameLong[newBankModel],
                }
            )
            return False

        # Check maximum amount
        bankClass = regbank.bankfile.BankFile.getClassForKeyboardName(newBankModel)

        if len(self.wndMain.oblNewBank) >= bankClass.maxReg:
            self.wndMain.setStatusMessage(const.msg["max-allowed-regs"] % (bankClass.maxReg))
            return False

        # Grant if nothing found
        return True


    def getDataNewBank(self):
        '''
        Callback function used by EasyDragAndDrop in order to query selected
        data dragged from "New Bank" list back to "Available Registrations"
        list.
        '''
        return self.wndMain.oblNewBank.get_selected()


    def getDataAvailableRegs(self):
        '''
        Callback function used by EasyDragAndDrop in order to query selected
        data dragged from "Available Registrations" list to "New Bank" list.
        '''
        return self.wndMain.oblAvailableRegs.get_selected()


    def copyColumn(self, src, dst, row):
        '''
        This method copies the given column from source ObjectList to
        destination ObjectList. It's not meant for direct use. Instead it's
        passed to an EasyDragAndDrop instance.
        '''
        dst.append(row.copy())
        self.wndMain.setStatusMessage(const.msg["added-to-bank"] % (row.name))

        # Emit newlist-changed signal
        if dst == self.wndMain.oblNewBank:
            self.emit("newlist-updated")


    def removeColumn(self, src, dst, row):
        '''
        This method removes the given column from the source ObjectList. It's
        not meant for direct use. Instead it's passed to an EasyDragAndDrop
        instance.
        '''
        if not row:
            return

        self.wndMain.oblNewBank.remove(row)
        self.wndMain.setStatusMessage(const.msg["removed-from-bank"] % (row.name))


    # User aids ...............................................................

    def checkAllowedButtons(self, *data):
        '''
        Event handler which reacts to several events. It checks which buttons
        after the event are valid and disables all invalid buttons.
        '''
        # Calculate button validity
        btnAdd    = True
        btnRemove = True
        btnBatch  = True
        btnSave   = True
        btnClear  = True
        btnUp     = True
        btnDown   = True

        if self.getNewBankKeyboardName() == const.UNKNOWN_MODEL \
        or self.getNewBankKeyboardName() == const.ALL_MODELS:
            btnAdd   = False
            btnBatch = False
            btnSave  = False

        if len(self.wndMain.oblNewBank) < 1:
            btnRemove = False
            btnClear  = False

        if len(self.wndMain.oblNewBank) < 2:
            btnUp     = False
            btnDown   = False

        if len(self.wndMain.oblAvailableRegs) < 2:
            # NOTE: ### EMPTY ### entry does always exist
            btnAdd   = False
            btnBatch = False

        # Disable invalid buttons
        self.wndMain.btnAddSelected.set_sensitive(btnAdd)
        self.wndMain.btnRemoveSelected.set_sensitive(btnRemove)
        self.wndMain.btnBatch.set_sensitive(btnBatch)
        self.wndMain.btnSaveBank.set_sensitive(btnSave)
        self.wndMain.btnClearList.set_sensitive(btnClear)
        self.wndMain.btnNewUp.set_sensitive(btnUp)
        self.wndMain.btnNewDown.set_sensitive(btnDown)
