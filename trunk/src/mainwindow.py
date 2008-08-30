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

# Public export of module content
__all__ = [
    "MainWindow",
    "AvailableRegsEntry",
    "ImportRegsEntry",
]


# Import system modules
from kiwi.ui.delegates     import GladeDelegate

import webbrowser
import os.path
import gtk
import sys

# Import application modules
import const
import main
import exceptiondialog
import createbanktab
import importregstab
import quickrenametab
import printsetlisttab
import informationtab
import abouttab


# Class definition
class MainWindow(GladeDelegate):
    '''
    This is the main window class.
    '''

    # List of controlled widgets
    widgets = [
        # Top level widgets
        "fcBtnDataDir",            # needs handler (current-folder-changed)
        "nbMain",
        "sbMain",

        # Create bank files page
        "evtAvailableRegs",
        "evtNewBankAvailFilter",
        "evtNewBank",
        "evtNewBankKeyModel",
        "vbbAvailableRegs",
        "btnAddSelected",          # needs handler (clicked)
        "btnRemoveSelected",       # needs handler (clicked)
        "btnBatch",                # needs handler (clicked)
        "vbbNewBank",
        "btnSaveBank",             # needs handler (clicked)
        "btnClearList",            # needs handler (clicked)
        "btnNewUp",                # needs handler (clicked)
        "btnNewDown",              # needs handler (clicked)

        # Import registrations page
        "evtImportRegs",
        "btnOpenBankFile",         # needs handler (clicked)
        "btnImportSelectedRegs",   # needs handler (clicked)
        "btnImportClear",          # needs handler (clicked)

        # Quick rename page
        "lblRenameRegs",
        "evtRenameRegs",
        "btnRenameOpen",           # needs handler (clicked)
        "btnRenameSave",           # needs handler (clicked)
        "btnRenameUp",             # needs handler (clicked)
        "btnRenameDown",           # needs handler (clicked)
        "btnRenameClear",          # needs handler (clicked)

        # Print setlist page
        "evtSetlist",
        "entSetlistName",
        "btnSetlistAdd",           # needs handler (clicked)
        "btnSetlistRemove",        # needs handler (clicked)
        "btnSetlistUp",            # needs handler (clicked)
        "btnSetlistDown",          # needs handler (clicked)
        "btnSetlistClear",         # needs handler (clicked)
        "btnSetlistPrint",         # needs handler (clicked)
        "btnSetlistExportText",    # needs handler (clicked)
        "btnSetlistExportCSV",     # needs handler (clicked)


        # Keyboard information page
        "lblKeyboards",

        # About page
        "imgAbout",
        "lblAbout",
        "linkAbout",               # needs handler (clicked)
        "lblThanks",
    ]


    # Create and display main window.............................................

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

        # Set window icon
        icon_filename = os.path.join(self.main.dataDir, "icon.png")
        self.wndMain.set_icon_from_file(icon_filename)

        # Set up status bar
        self.sbContext   = self.sbMain.get_context_id("main")
        self.sbLastMsgId = 0
        self.setStatusMessage(const.msg["ready"])

        # Set directory chooser's current path
        self.fcBtnDataDir.set_filename(self.main.workDir)

        # Prepare delegates for driving the tab's contents
        self.createBankTab   = createbanktab.CreateBankTab(wndMain=self)
        self.importRegsTab   = importregstab.ImportRegsTab(wndMain=self)
        self.quickRenameTab  = quickrenametab.QuickRenameTab(wndMain=self)
        self.printSetlistTab = printsetlisttab.PrintSetlistTab(wndMain=self)
        self.informationTab  = informationtab.InformationTab(wndMain=self)
        self.aboutTab        = abouttab.AboutTab(wndMain=self)


    def run(self):
        '''
        Shows the main window and starts the main event loop.
        '''
        # Set up exception hook dialog
        sys.excepthook = lambda type, value, traceback: self.showExceptionDialog(type, value, traceback)

        # Run GTK+ event loop
        self.show_and_loop()


    def showExceptionDialog(self, type, value, traceback):
        '''
        Exception hook which catches all exception not handled otherwise by
        the program. Opens a dialog with an explaining text and traceback. The
        dialog allows to save the traceback to a file for reporting back.
        '''
        dlg = exceptiondialog.ExceptionDialog(type, value, traceback)
        dlg.show()

        return True


    def setStatusMessage(self, msg):
        '''
        This method sets the text displayed in the status bar.
        '''
        # Remove previous mesage from statusbar's stack (saves memory)
        if self.sbLastMsgId:
            self.sbMain.remove(self.sbContext, self.sbLastMsgId)

        # Push new message onto statusbar
        self.sbLastMsgId = self.sbMain.push(self.sbContext, msg)


    # Main window event handlers...............................................

    def updateAvailableRegList(self):
        '''
        This method updates the list of available registrations.
        '''
        self.createBankTab.on_main__work_dir_changed(None, self.main.workDir)


    def on_wndMain__destroy(self, *args):
        '''
        Event handler called at destroyment of the main window. Usually this
        will also be the application's end.
        '''
        # Manually decrese main loop nesting level.
        # ATTENTION: This is needed due to the file chooser button which
        # silently increases the main loop level by one. The effect of this
        # is that Kiwi's quit_on_last doesn't really quit the application
        # but leaves it running within a spare main loop.
        gtk.main_quit()


    def on_fcBtnDataDir__current_folder_changed(self, *args):
        '''
        Event handler for responding on the user having changed the data (work)
        directory. Calls self.main.setWorkDir() which in turn emits a
        work-dir-changed signal.
        '''
        # Leave of directory hasn't been changed
        if self.main.workDir == args[0].get_filename():
            return

        # Remember directory and emit notification signal
        self.main.setWorkDir(args[0].get_filename())

        # Give message on the statusbar
        self.setStatusMessage(const.msg["changed-dir"] % (self.main.workDir))


    # Event handlers for "Create bank file" page...............................

    def on_btnAddSelected__clicked(self, *args):
        '''
        Evemt handler for the add selected button. Delegates the call to an
        object of type CreateBankTab.
        '''
        self.createBankTab.addSelectedItemsToExport()


    def on_btnRemoveSelected__clicked(self, *args):
        '''
        Event handler for remove selected button. Delegates the call to an
        object of type CreateBankTab.
        '''
        self.createBankTab.removeSelectedItemsFromExportList()


    def on_btnBatch__clicked(self, *args):
        '''
        Event handler for batch processing button. Delegates the coll to an
        object of type CreateBankTab.
        '''
        self.createBankTab.doBatch()


    def on_btnSaveBank__clicked(self, *args):
        '''
        Event handler for save bank button. Delegates the call to an
        object of type CreateBankTab.
        '''
        self.createBankTab.saveBankFile()


    def on_btnClearList__clicked(self, *args):
        '''
        Event handler for remove all button. Delegates the call to an object
        of type CreateBankTab.
        '''
        self.createBankTab.removeAllItemsFromExportList()


    def on_btnNewUp__clicked(self, *args):
        '''
        Event handler for moving a registration within a bank file up.
        '''
        self.createBankTab.newBankMoveSelectedUp()


    def on_btnNewDown__clicked(self, *args):
        '''
        Event handler for moving a registration within a bank file down.
        '''
        self.createBankTab.newBankMoveSelectedDown()


    # Event handlers from "Import Registrations" page..........................

    def on_btnOpenBankFile__clicked(self, *args):
        '''
        Event handler for the open bank file button. Delegates the call to an
        object of type ImportRegsTab.
        '''
        self.importRegsTab.openBankFile()


    def on_btnImportSelectedRegs__clicked(self, *args):
        '''
        Event handler for import selected regs button. Delegates the call to an
        object of type ImportRegsTab.
        '''
        self.importRegsTab.importSelectedRegs()


    def on_btnImportClear__clicked(self, *args):
        '''
        Event handler for the "Clear Import List" button. Delegates the call to
        an ImportRegsTab object.
        '''
        self.importRegsTab.clearList()


    # Event handlers for "Quick Rename" page...................................
    def on_btnRenameOpen__clicked(self, *args):
        '''
        Event handler for "Open Bank File..." button on the quick rename page.
        Delegates the call to an QuickRenameTab object.
        '''
        self.quickRenameTab.openBankFile()


    def on_btnRenameSave__clicked(self, *args):
        '''
        Event handler for "Save" button on the quick rename page. Delegates
        the call to an QuickRenameTab object.
        '''
        self.quickRenameTab.saveBankFile()


    def on_btnRenameUp__clicked(self, *args):
        '''
        Event handler for "Up" button on the quick rename page. Delegates
        the call to an QuickRenameTab object.
        '''
        self.quickRenameTab.moveSelectedUp()


    def on_btnRenameDown__clicked(self, *args):
        '''
        Event handler for "Down" button on the quick rename page. Delegates
        the call to an QuickRenameTab object.
        '''
        self.quickRenameTab.moveSelectedDown()


    def on_btnRenameClear__clicked(self, *args):
        '''
        Event handler for "Clear" button on the quick rename page. Delegates
        the call to an QuickRenameTab object.
        '''
        self.quickRenameTab.clearList()


    # Event handlers for "Print Setlist" page..................................

    def on_btnSetlistAdd__clicked(self, *args):
        '''
        Event handler for the Add button on the print setlist page.
        Delegates the call to a PrintSetlistTab object.
        '''
        self.printSetlistTab.addBankFile()


    def on_btnSetlistRemove__clicked(self, *args):
        '''
        Event handler for the Remove button on the print setlist page.
        Delegates the call to a PrintSetlistTab object.
        '''
        self.printSetlistTab.removeSelected()


    def on_btnSetlistUp__clicked(self, *args):
        '''
        Event handler for the ### button on the print setlist page.
        Delegates the call to a PrintSetlistTab object.
        '''
        self.printSetlistTab.moveSelectedUp()


    def on_btnSetlistDown__clicked(self, *args):
        '''
        Event handler for the Down button on the print setlist page.
        Delegates the call to a PrintSetlistTab object.
        '''
        self.printSetlistTab.moveSelectedDown()


    def on_btnSetlistClear__clicked(self, *args):
        '''
        Event handler for the Clear button on the print setlist page.
        Delegates the call to a PrintSetlistTab object.
        '''
        self.printSetlistTab.clearList()


    def on_btnSetlistPrint__clicked(self, *args):
        '''
        Event handler for the Print button on the print setlist page.
        Delegates the call to a PrintSetlistTab object.
        '''
        self.printSetlistTab.export("PRINT")


    def on_btnSetlistExportText__clicked(self, *args):
        '''
        Event handler for the ExportText button on the print setlist page.
        Delegates the call to a PrintSetlistTab object.
        '''
        self.printSetlistTab.export("TEXT")


    def on_btnSetlistExportCSV__clicked(self, *args):
        '''
        Event handler for the Export CSV button on the print setlist page.
        Delegates the call to a PrintSetlistTab object.
        '''
        self.printSetlistTab.export("CSV")


    # Event handlers for "About" page..........................................

    def on_linkAbout__clicked(self, *args):
        '''
        Event handle for the link button on the about pane. Tries to open
        the website URI as given by const.url in a browser.
        '''
        # Open website URI in browser
        success = webbrowser.open(const.url)

        # Give message on the statusbar
        if success:
            self.setStatusMessage(const.msg["browser-opened"])
        else:
            self.setStatusMessage(const.msg["browser-not-opened"])


# Class definition of list entries
class AvailableRegsEntry:
    '''
    List entry class for the "Available Registrations" list. Holds the
    following values:

    * name,     Name of the registration
    * keyname,  Long name of the keyboard model
    * model,    Internal name of the keyboard model
    * filename, File name of the registration file
    '''

    def __init__(self, name="", keyName="", model="", fileName=""):
        '''
        Constructor. Just stores the given parameters.
        '''
        self.name     = name
        self.keyName  = keyName
        self.model    = model
        self.fileName = fileName

    def copy(self):
        '''
        Returns a flat copy of the object.
        '''
        return self.__class__(
            name     = self.name,
            keyName  = self.keyName,
            model    = self.model,
            fileName = self.fileName
        )


class ImportRegsEntry:
    '''
    List entry class for the "Import Registrations" list. Holds the following
    values which can all be accessed from the list.

    * mark,  Boolean check
    * pos,   Position in registration bank
    * name,  Name of registration
    * model, Internal name of the keyboard model
    * reg,   Registration Object
    '''

    def __init__(self, mark=False, pos=0, name="", model="", regObj=None):
        '''
        Constructor. Just stores the given parameters.
        '''
        self.mark   = mark
        self.pos    = pos
        self.name   = name
        self.model  = model
        self.regObj = regObj

    def copy(self):
        '''
        Returns a flat copy of the object.
        '''
        return self.__class__(
            mark   = self.mark,
            pos    = self.pos,
            name   = self.name,
            model  = self.model,
            regObj = self.regObj
        )
