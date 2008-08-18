#encoding=utf-8

# batchdialog.py
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

This module provides a controller class for batch creation of registration
banks. This class does both: Controling the GTK-dialog and doing the
processing.
'''

# Public export of module content
__all__ = [
    "BatchDialog"
]

# Import global modules
from kiwi.ui.delegates     import GladeDelegate
from kiwi.ui.widgets.combo import ProxyComboBox

import os.path

# Import application modules
import const
import main
import appexceptions
import regbank.bankfile


# Class definition
class BatchDialog(GladeDelegate):
    '''
    This class controls the batch processing dialog and performs the actual
    processing.
    '''

    # List of controlled widgets
    widgets = [
        "lblBatchSortBy",
        "evtBatchSortBy",
        "fcBtnBatchSave",
        "entBatchFilename",
        "btnBatchCancel",          # needs handler (clicked)
        "btnBatchExecute",         # needs handler (clicked)
    ]

    # Dialog life-cycle .......................................................

    def __init__(self, keyboardName, regEntryList):
        '''
        Default constructor. Sets up the dialog but doesn't show it.
        '''
        # Store keyboard name and find appropriate class
        self.keyboardName  = keyboardName
        self.bankFileClass = regbank.bankfile.BankFile.getClassForKeyboardName(keyboardName)

        # Store registration list
        self.regEntryList = regEntryList

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
            toplevel_name  = "dlgBatch",
            delete_handler = self.hide_and_quit
        )

        # Set window icon
        icon_filename = os.path.join(self.main.dataDir, "icon.png")
        self.dlgBatch.set_icon_from_file(icon_filename)

        # Insert combobox with available sort criteria
        self.cbxBatchSortBy = ProxyComboBox()
        self.evtBatchSortBy.add(self.cbxBatchSortBy)
        self.cbxBatchSortBy.show()

        self.cbxBatchSortBy.append_item(_("Registration name (ascending)"),  const.SORT_BY_NAME_ASC)
        self.cbxBatchSortBy.append_item(_("Registration name (descending)"), const.SORT_BY_NAME_DESC)
        self.cbxBatchSortBy.append_item(_("Random order"), const.SORT_RANDOM)

        self.cbxBatchSortBy.select(const.SORT_BY_NAME_ASC)
        self.cbxBatchSortBy.update(const.SORT_BY_NAME_ASC)

        self.lblBatchSortBy.set_mnemonic_widget(self.cbxBatchSortBy)

        # Set default filename pattern
        suggestion = "&n - &hash.%s" % (self.bankFileClass.fileExt)
        self.entBatchFilename.set_text(suggestion)

        # Connect to signals for execute-disabling
        self.cbxBatchSortBy.connect("content-changed", self.disable_execute_button)


    def show(self):
        '''
        Shows and runs the batch dialog in a modal fashion. Triggers batch
        processing of the dialog successfuly resolves.
        '''
        response = self.dlgBatch.run()

        if response > 0:
            self.process()

        self.dlgBatch.hide()


    def destroy(self):
        '''
        Use this method as a sort-of-destructor. Makes sure the dialog
        gets destroyed and its occupied memory freed.
        '''
        self.dlgBatch.destroy()


    # Enable / Disable execute button .........................................

    def disable_execute_button(self, widget=None, *data):
        '''
        Event handler method which disables or enables the execute button
        depending on whether all fields are set.
        '''
        filenamePattern = self.entBatchFilename.get_text()
        if  self.cbxBatchSortBy.read()          \
        and self.fcBtnBatchSave.get_filename()  \
        and (filenamePattern.find("&n") >= 0 or filenamePattern.find("&hash") >= 0):
            sensitive = True
        else:
            sensitive = False

        self.btnBatchExecute.set_sensitive(sensitive)


    def on_fcBtnBatchSave__current_folder_changed(self, *args):
        '''
        Event handler which reacts to changed destination directory. Checks
        whether the execute button can be enabled or not.
        '''
        self.disable_execute_button()


    def on_entBatchFilename__changed(self, widget, *data):
        '''
        Event handler which reacts to a changed filename pattern. Checks
        whether the execute button can be enabled or not.
        '''
        self.disable_execute_button()


    # Batch processing ........................................................

    def process(self):
        '''
        This method performs the actual processing.

        ATTENTION: NOT YET IMPLEMENTED !!!
        '''
        pass
