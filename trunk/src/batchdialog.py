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

import os
import os.path
import random

# Import application modules
import const
import main
import appexceptions

import regbank.bankfile
import regfile.regfile
import regfile.appexceptions
import regbank.appexceptions


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
        suggestion = "(&n&) &hash&.%s" % (self.bankFileClass.fileExt)
        self.entBatchFilename.set_text(suggestion)

        # Connect to signals for execute-disabling
        self.cbxBatchSortBy.connect("content-changed", self.disable_execute_button)


    def show(self):
        '''
        Shows and runs the batch dialog in a modal fashion. Triggers batch
        processing if the dialog successfuly resolves.
        '''
        amount   = 0
        response = self.dlgBatch.run()

        if response > 0:
            sortCriterion = self.cbxBatchSortBy.get_selected()
            savePath      = self.fcBtnBatchSave.get_filename()
            namePattern   = self.entBatchFilename.get_text()

            amount = self.process(sortCriterion, savePath, namePattern)

            self.dlgBatch.hide()
            return amount
        else:
            self.dlgBatch.hide()
            raise appexceptions.Cancel()


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
        # Assure all fields are filed (inlcuding filename variables)
        filenamePattern = self.entBatchFilename.get_text()
        if  self.cbxBatchSortBy.read()          \
        and self.fcBtnBatchSave.get_filename()  \
        and (filenamePattern.find("&n&") >= 0 or filenamePattern.find("&hash&") >= 0):
            sensitive = True
        else:
            sensitive = False

        # Assure the filename pattern doesn't contain paths
        if filenamePattern.find(os.sep) >= 0:
            sensitive = False

        self.btnBatchExecute.set_sensitive(sensitive)


    def on_fcBtnBatchSave__current_folder_changed(self, *args):
        '''
        Event handler which reacts to changed destination directory. Checks
        whether the execute button can be enabled or not. Also changes the
        processe's working directory so that file dialogs don't loose the
        last directory.
        '''
        # Check valid buttons
        self.disable_execute_button()

        # Set processe's working directory
        os.chdir(self.fcBtnBatchSave.get_filename())


    def on_entBatchFilename__changed(self, widget, *data):
        '''
        Event handler which reacts to a changed filename pattern. Checks
        whether the execute button can be enabled or not.
        '''
        self.disable_execute_button()


    # Batch processing ........................................................

    def process(self, sortCriterion, savePath, namePattern):
        '''
        This method performs the actual processing. It returns the amount of
        created bank files.
        '''
        # Sort list by selected criterion
        if sortCriterion == const.SORT_BY_NAME_ASC:
            # Sort by name (ascending)
            self.regEntryList.sort(key=lambda e: e.name.upper())
        elif sortCriterion == const.SORT_BY_NAME_DESC:
            # Sort by name (descending)
            self.regEntryList.sort(key=lambda e: e.name.upper(), reverse=True)
        else:
            # Random order
            random.shuffle(self.regEntryList)

        # Create bank files
        storeEntries = []
        regsPerBank  = self.bankFileClass.maxReg
        amountFiles  = 0

        while self.regEntryList:
            # Remember adjacend registration names from adjacent packages
            try:
                leadingName = storeEntries[len(storeEntries) - 1].name
            except IndexError:
                # First run
                leadingName = ""

            try:
                trailingName = self.regEntryList[regsPerBank].name
            except IndexError:
                # Last run
                trailingName = ""

            # Slice out next package
            storeEntries = self.regEntryList[:regsPerBank]
            self.regEntryList = self.regEntryList[regsPerBank:]

            if not storeEntries:
                break

            # Remember first and last name of current package
            firstName = storeEntries[0].name
            lastName  = storeEntries[len(storeEntries) - 1].name

            # Create registration objects
            regList = []

            for regEntry in storeEntries:
                try:
                    regFile = regfile.regfile.RegFile(filename=regEntry.fileName)
                    regObj  = regFile.getRegistrationObject()
                except regfile.appexceptions.UnknownFileFormat:
                    regObj = None
                except regbank.appexceptions.UnknownKeyboardModel:
                    rebObj = None

                regList.append(regObj)

            # Calculate filename
            amountFiles += 1
            hash = self.hash_names(leadingName, firstName, lastName, trailingName)

            filename = namePattern
            filename = filename.replace("&n&", str(amountFiles))
            filename = filename.replace("&hash&", hash)

            filename = os.path.join(savePath, filename)

            # Store bank file
            bankFile = self.bankFileClass(keyboardName=self.keyboardName)
            bankFile.setRegistrationObjects(regList)
            bankFile.storeBankFile(filename=filename)

        # Return amount of created bank files
        return amountFiles


    def hash_names(self, leading, first, last, trailing):
        '''
        This method calculates the &hash& value for filename patterns. It
        tries to find a value like »Abc - Xyz« which contains the first letters
        of the given first and last name. For this it takes the leading and
        trailing names in account in order to calculate a most distinguishing
        hash value.
        '''
        # Left value
        wordsLeading = leading.split()
        wordsFirst   = first.split()

        if not wordsLeading:
            wordsLeading = [""]

        if not wordsFirst:
            wordsFirst = [""]

        words = self.distinguish(wordsFirst, wordsLeading)
        leftValue = ""

        for word in words:
            if leftValue:
                leftValue += " "

            leftValue += word

        # Right value
        wordsLast     = last.split()
        wordsTrailing = trailing.split()

        if not wordsLast:
            wordsLast = [""]

        if not wordsTrailing:
            wordsTrailing = [""]

        words = self.distinguish(wordsLast, wordsTrailing)
        rightValue = ""

        for word in words:
            if rightValue:
                rightValue += " "

            rightValue += word

        # Complete value
        return "%s - %s" % (leftValue, rightValue)


    def distinguish(self, list1, list2):
        '''
        Compares two sequences and returns a new sequence which contains
        all the common begining of both list plus one entry from list one.
        '''
        distinguish = []

        for pos in range(len(list1)):
            try:
                distinguish.append(list1[pos])

                if not list1[pos] == list2[pos]:
                    break
            except IndexError:
                break

        return distinguish
