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

# Import system modules
from kiwi.ui.delegates import GladeDelegate
import webbrowser
import os.path
import gtk

# Import application modules
import const
import main
import createbanktab
import importregstab


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
        "treeAvailableRegs",
        "treeNewBank",
        "btnSaveBank",             # needs handler (clicked)
        "btnRemoveSelected",       # needs handler (clicked)
        "btnClearList",            # needs handler (clicked)

        # Import registrations pane
        "treeImportRegs",
        "btnOpenBankFile",         # needs handler (clicked)
        "btnImportSelectedRegs",   # needs handler (clicked)

        # About pane
        "imgAbout",
        "lblAbout",
        "linkAbout"                # needs handler (clicked)
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
            "licence":  const.copyright_long
        }

        self.lblAbout.set_use_markup(True)
        self.lblAbout.set_markup(about_txt)

        self.linkAbout.set_label(_("Click here for more information"))
        self.linkAbout.set_uri(const.url)

        # Prepare delegates for driving the tab's contents
        self.createBankTab = createbanktab.CreateBankTab(wndMain=self)
        self.importRegsTab = importregstab.ImportRegsTab(wndMain=self)


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


    def on_btnSaveBank__clicked(self, *args):
        '''
        Event handler for save bank button. Delegates the call to an
        object of type CreateBankTab.
        '''
        self.createBankTab.saveBankFile()


    def on_btnRemoveSelected__clicked(self, *args):
        '''
        Event handler for remove selected button. Delegates the call to an
        object of type CreateBankTab.
        '''
        self.createBankTab.removeSelectedItemsFromExportList()


    def on_btnClearList__clicked(self, *args):
        '''
        Event handler for remove all button. Delegates the call to an object
        of type CreateBankTab.
        '''
        self.createBankTab.removeAllItemsFromExportList()


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
