#encoding=utf-8

# printsetlisttab.py
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

This module provides a controller class which coordinates the printing of
bank file contents. The main window class acts as some bridge here as this is
the class which receives all events on the tab page and which delegates them
over here.
'''

# Public export of module content
__all__ = [
    "ExportSetlistTab"
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
import exportsetlist.exportbase
import exportsetlist.appexceptions
import regbank.bankfile
import appexceptions
import mainwindow
import main
import util
import const


# Class definition
class ExportSetlistTab(gobject.GObject):
    '''
    This delegate class allows to print the contents of bank files.

    Emited signals:
    ---------------

    *setlist-updated*: Emited after the bank file list has changed.
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
            "setlist-updated",
            ExportSetlistTab,
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
        self.oblSetlist = ObjectList(
            [
                Column("shortname", title=_("Bank File"), order=gtk.SORT_ASCENDING, searchable=True, expand=True),
                Column("keyName",   title=_("Keyboard"),  order=gtk.SORT_ASCENDING),
            ]
        )

        self.wndMain.evtSetlist.add(self.oblSetlist)
        self.oblSetlist.show()

        self.oblSetlist.connect("has-rows", self.onListEmptyChanged)
        self.connect("setlist-updated", self.onListUpdated)

        # Create export action popup menu
        self.goMenu = gtk.Menu()
        self.goMenu.attach_to_widget(self.wndMain.btnSetlistGo, None)

        classes = exportsetlist.exportbase.ExportBase.getExporterClasses()
        classes.sort(key=lambda c: c.displayName.upper())

        for cls in classes:
            menuItem = gtk.MenuItem(cls.displayName, True)
            menuItem.connect("activate", self.onGoMenuItemActivated, cls)
            menuItem.show()

            self.goMenu.append(menuItem)

        # Add images to buttons
        img = gtk.Image()
        img.set_from_stock(gtk.STOCK_ADD, gtk.ICON_SIZE_BUTTON)
        self.wndMain.btnSetlistAdd.set_property("image_position", gtk.POS_TOP)
        self.wndMain.btnSetlistAdd.set_image(img)

        img = gtk.Image()
        img.set_from_stock(gtk.STOCK_REMOVE, gtk.ICON_SIZE_BUTTON)
        self.wndMain.btnSetlistRemove.set_property("image_position", gtk.POS_TOP)
        self.wndMain.btnSetlistRemove.set_image(img)

        img = gtk.Image()
        img.set_from_stock(gtk.STOCK_CLEAR, gtk.ICON_SIZE_BUTTON)
        self.wndMain.btnSetlistClear.set_property("image_position", gtk.POS_TOP)
        self.wndMain.btnSetlistClear.set_image(img)

        # Assume empty list
        self.oblSetlist.clear()
        self.onListEmptyChanged(self.oblSetlist, False)


    # Management of list content...............................................

    def addBankFile(self):
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

        # Add bank file to the list
        bankEntry = SetlistEntry(
            filename = filename,
            model    = keyModel,
            keyName  = const.keyboardNameLong[keyModel],
            bankObj  = regBankObj
        )

        self.oblSetlist.append(bankEntry)

        # Emit setlist-updated signal
        self.emit("setlist-updated", self.oblSetlist)

        # Show success message
        self.wndMain.setStatusMessage(const.msg["bank-add-success"] % {
                "filename": filename,
            }
        )


    def removeSelected(self):
        '''
        Delegate method called by the UI. Removes the selected item from
        the setlist.
        '''
        entry = self.oblSetlist.get_selected()

        if not entry:
            return

        self.oblSetlist.remove(entry)

        # Emit setlist-updated signal
        self.emit("setlist-updated", self.oblSetlist)


    def clearList(self):
        '''
        Delegate method called by the UI. Clears the import list.
        '''
        self.oblSetlist.clear()
        self.wndMain.entSetlistName.set_text("")


    def moveSelectedUp(self):
        '''
        Delegate method called by the UI. Moves the selected entry up by
        one position.
        '''
        # Move selected entry up
        pos = self.oblSetlist.get_selected_row_number()

        if not pos or pos < 1:
            return

        row = self.oblSetlist.get_selected()
        self.oblSetlist.remove(row)

        self.oblSetlist.insert(
            index    = pos - 1,
            instance = row,
            select   = True
        )

        # Give short success message
        self.wndMain.setStatusMessage(const.msg["moved-one-up"] % (row.shortname))


    def moveSelectedDown(self):
        '''
        Delegate method called by the UI. Moves the selected entry down by
        one position.
        '''
        # Move selected entry down
        pos = self.oblSetlist.get_selected_row_number()

        if pos < 0 or pos >= len(self.oblSetlist) - 1:
            return

        row = self.oblSetlist.get_selected()
        self.oblSetlist.remove(row)

        self.oblSetlist.insert(
            index    = pos + 1,
            instance = row,
            select   = True
        )

        # Give short success message
        self.wndMain.setStatusMessage(const.msg["moved-one-down"] % (row.shortname))


    # Export...................................................................

    def showGoMenu(self):
        '''
        Delegate method called by the UI. Shows a popup menu with all available
        export and print actions.
        '''
        self.goMenu.popup(None, None, None, 0, 0)


    def onGoMenuItemActivated(self, menuItem, exportClass):
        '''
        Event handler method which gets called whenever the user activates
        a menu entry in the Go! popup menu. Delegates the call to the export
        method.
        '''
        self.export(exportClass)


    def export(self, exportClass):
        '''
        This method uses the given class in order to export the setlist. The
        class must be a sub-class of exportsetlist.exportbase.ExportBase.
        Otherwise appexceptions.InvalidExportClass gets thrown.
        '''
        # Perform export
        try:
            # Get name of setlist
            printName = self.wndMain.entSetlistName.get_text()

            # Check class validity
            if not issubclass(exportClass, exportsetlist.exportbase.ExportBase):
                raise appexceptions.InvalidExportClass(exportClass)

            # Process
            exportObj = exportClass(
                wndMain = self.wndMain,
                printName = printName,
                setlistEntries = self.oblSetlist[:]
            )

            successMsg = exportObj.do()

            # Give success message
            if successMsg:
                self.wndMain.setStatusMessage(successMsg)
        except exportsetlist.appexceptions.Cancel:
            pass


    # Widget event handerls.....................................................

    def onListEmptyChanged(self, list, hasRows):
        '''
        Delegate method called by the UI whenever the list of registrations
        to be imported changes its empty state. Used to disable or enable
        buttons.
        '''

        # Set buttons (in)active
        self.wndMain.btnSetlistRemove.set_sensitive(hasRows)
        self.wndMain.btnSetlistClear.set_sensitive(hasRows)
        self.wndMain.btnSetlistGo.set_sensitive(hasRows)

        # Emit setlist-updated signal
        self.emit("setlist-updated", list)


    def onListUpdated(self, tab, *list):
        '''
        Event handler which responds to the list being updated. Used to control
        move up and down buttons.
        '''
        moreThanOne = len(list[0]) > 1
        self.wndMain.btnSetlistUp.set_sensitive(moreThanOne)
        self.wndMain.btnSetlistDown.set_sensitive(moreThanOne)


# Class definition for list contents
class SetlistEntry:
    '''
    This class defines the list entries for the print setlist oage. Holds
    the following values:

    * filename, Name of the bank file
    * model,    Technical description of keyboard model
    * keyName,  User-description of keyboard model
    * bankObj,  A BankFile object
    '''

    def __init__(self, filename="", model="", keyName="", bankObj=None):
        '''
        Constructor. Just stores the given parameters
        '''
        shortname = os.path.split(filename)[1]
        if bankObj:
            shortname = bankObj.stripName(shortname)

        self.filename  = filename
        self.shortname = shortname
        self.model     = model
        self.keyName   = keyName
        self.bankObj   = bankObj
