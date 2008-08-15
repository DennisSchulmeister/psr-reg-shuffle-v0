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
from kiwi.ui.objectlist    import ObjectList
from kiwi.ui.objectlist    import Column
from kiwi.ui.widgets.combo import ProxyComboBox

import webbrowser
import os.path
import gtk

# Import application modules
import const
import main
import createbanktab
import importregstab


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

        # Create bank files pane
        "evtAvailableRegs",
        "evtNewBank",
        "evtNewBankKeyModel",
        "btnAddSelected",          # needs handler (clicked)
        "btnSaveBank",             # needs handler (clicked)
        "btnRemoveSelected",       # needs handler (clicked)
        "btnClearList",            # needs handler (clicked)
        "btnNewUp",                # needs handler (clicked)
        "btnNewDown",              # needs handler (clicked)

        # Import registrations pane
        "evtImportRegs",
        "btnOpenBankFile",         # needs handler (clicked)
        "btnImportSelectedRegs",   # needs handler (clicked)

        # About pane
        "imgAbout",
        "lblAbout",
        "linkAbout",               # needs handler (clicked)
        "lblThanks",
    ]


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
        self.setStatusMessage(_("Ready."))

        # Set directory chooser's current path
        self.fcBtnDataDir.set_filename(self.main.workDir)

        # Set image and text of about pane
        logo_filename = os.path.join(self.main.dataDir, "logo_medium.png")
        self.imgAbout.set_from_file(logo_filename)

        about_txt = "<big><big><big><b>%(progname)s %(version)s</b></big></big></big>\n<i>%(descr)s</i>\n\n%(licence)s" % \
        {
            "progname": const.progname,
            "version":  const.version,
            "descr":    const.description,
            "licence":  const.copyright_long,
            "thanks":   const.thanks,
        }

        self.lblAbout.set_use_markup(True)
        self.lblAbout.set_markup(about_txt)

        self.linkAbout.set_label(const.url)
        self.linkAbout.set_uri(const.url)

        self.lblThanks.set_use_markup(True)
        self.lblThanks.set_markup(const.thanks)

        # Insert ObjectLists into the main window
        self.oblAvailableRegs = ObjectList(
            [
                Column("name",    title=_("Registration Name"), order=gtk.SORT_ASCENDING, searchable=True, editable=True, expand=True),
                Column("keyName", title=_("Keyboard"), order=gtk.SORT_ASCENDING),
            ],
            sortable = True
        )

        self.oblNewBank = ObjectList(
            [
                Column("name", title=_("Registration Name"), order=-1, searchable=True, editable=True, expand=True),
            ]
        )

        self.oblImportRegs = ObjectList(
            [
                Column("mark", title=_("Import"), data_type=bool, editable=True),
                Column("pos",  title=_("Number"), editable=False),
                Column("name", title=_("Registration Name"), editable=True, searchable=True, expand=True),
            ]
        )

        self.evtAvailableRegs.add(self.oblAvailableRegs)
        self.evtNewBank.add(self.oblNewBank)
        self.evtImportRegs.add(self.oblImportRegs)

        self.oblAvailableRegs.show()
        self.oblNewBank.show()
        self.oblImportRegs.show()

        try:
            self.oblAvailableRegs.enable_dnd()
            self.oblNewBank.enable_dnd()
        except AttributeError:
            # Work around mising DnD-support in older kiwi versions
            pass

        # NOTE: Don't set the TreeView reorderable except you're in for some
        # nasty exceptions if someone really tries to reorder the tree.
        ## self.oblNewBank.get_treeview().set_reorderable(True)

        self.oblAvailableRegs.connect("cell-edited", self.on_oblAvailableRegs_cell_edited)
        self.oblNewBank.connect("has-rows", self.on_oblNewBank_has_rows)

        # Insert combobox for selecting keyboard model of new bank files
        self.cbxNewBankKeyModel = ProxyComboBox()
        self.evtNewBankKeyModel.add(self.cbxNewBankKeyModel)
        self.cbxNewBankKeyModel.show()

        # Prepare delegates for driving the tab's contents
        self.createBankTab = createbanktab.CreateBankTab(wndMain=self)
        self.importRegsTab = importregstab.ImportRegsTab(wndMain=self)

        # Connect to content-changed of keyboard model combobox
        # NOTE: Must be after initialization of delegates above because the
        # signal will be triggered right after connecting.
        self.cbxNewBankKeyModel.connect("content-changed", self.on_cbxNewBankKeyModek_content_changed)


    def run(self):
        '''
        Shows the main window and starts the main event loop.
        '''
        self.show_and_loop()


    def setStatusMessage(self, msg):
        '''
        This method sets the text displayed in the status bar.
        '''
        # Remove previous mesage from statusbar's stack (saves memory)
        if self.sbLastMsgId:
            self.sbMain.remove(self.sbContext, self.sbLastMsgId)

        # Push new message onto statusbar
        self.sbLastMsgId = self.sbMain.push(self.sbContext, msg)


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
        self.setStatusMessage(_("Changed directory to %s." % (self.main.workDir)))


    def on_oblAvailableRegs_cell_edited(self, *args):      # Manually connected
        '''
        Event handler which responds whenever the user edits the name of
        an available registration. The change will be stored to the associated
        regfile which will also renamed.
        '''
        self.createBankTab.availableRegRename(args[1])


    def on_cbxNewBankKeyModek_content_changed(self, widget):
        '''
        Event handler which gets triggered whenever the user changes the
        keyboard model of a new registration bank. The call gets delegated
        to a CreateBankTab object.
        '''
        self.createBankTab.onKeyboardModelChanged(widget)


    def on_oblNewBank_has_rows(self, list, hasRows):
        '''
        Event handler which gets triggered whenever a new bank goes from
        empty to non-empty or vice versa. The call gets delegated to a
        CreateBankTab object.
        '''
        self.createBankTab.onNewBankEmptyChanged(list, hasRows)


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


    def on_linkAbout__clicked(self, *args):
        '''
        Event handle for the link button on the about pane. Tries to open
        the website URI as given by const.url in a browser.
        '''
        # Open website URI in browser
        success = webbrowser.open(const.url)

        # Give message on the statusbar
        if success:
            self.setStatusMessage(_("Sucessfully opened web browser."))
        else:
            self.setStatusMessage(_("Unable to launch web browser."))


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
