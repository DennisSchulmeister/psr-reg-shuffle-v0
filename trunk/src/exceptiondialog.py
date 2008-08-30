#encoding=utf-8

# exceptiondialog.py
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

This module provides a dialog which can be called within the sys.excepthook
in order to show exceptions to the user.
'''

# Public export of module content
__all__ = [
    "ExceptionDialog"
]

# Import global modules
from kiwi.ui.delegates import GladeDelegate
import kiwi.ui.dialogs
import gtk

import sys
import os.path
import traceback
import StringIO

# Import application modules
import main


# Class definition
class ExceptionDialog(GladeDelegate):
    '''
    This class provied a dialog window which can be displayed within the
    sys.excepthook.
    '''

    # List of controlled widgets
    widgets = [
        "lblExcMessage",
        "lblExcTraceback",
        "btnExcSave",
        "fcBtnBatchSave",          # needs handler (clicked)
    ]

    # Dialog life-cycle .......................................................

    def __init__(self, type, value, traceback):
        '''
        Default constructor. Sets up the dialog but doesn't show it.
        '''
        # Store exception data
        self.type      = type
        self.value     = value
        self.traceback = traceback

        # Calculate needed data
        # NOTE: Kiwi provides its own way of finding glade files. In fact
        # the main.dataDir has been added to Kiwi's search path by the main
        # singleton object so it's not needed here. Kiwi would ignore it
        # anway if the gladefile path was to include it.
        self.main      = main.Main.getInstance()
        self.wndMain   = self.main.wnd
        self.gladefile = "ui.glade"

        # Load glade file
        GladeDelegate.__init__(
            self,
            gladefile      = self.gladefile,
            toplevel_name  = "dlgException",
            delete_handler = self.hide_and_quit
        )

        # Set window icon
        icon_filename = os.path.join(self.main.dataDir, "icon.png")
        self.dlgException.set_icon_from_file(icon_filename)

        # Set icon of save button
        img = gtk.Image()
        img.set_from_stock(gtk.STOCK_SAVE_AS, gtk.ICON_SIZE_BUTTON)
        self.btnExcSave.set_image(img)

        # Set message text
        # NOTE: Cannot retrieve traceback text here.
        msg = str(value)
        msg = msg.replace("&", "&amp;")
        msg = msg.replace("<", "&lt;")
        msg = msg.replace(">", "&gt;")

        self.lblExcMessage.set_markup("<big><i>%s</i></big>" % msg)


    def show(self):
        '''
        Shows and runs the batch dialog in a modal fashion. Triggers batch
        processing if the dialog successfuly resolves.
        '''
        # Call default exception hook to get traceback on strdout
        sys.__excepthook__(self.type, self.value, self.traceback)

        # Set traceback text
        # NOTE: Aparently this cannot be done w/o executing the default
        # excepthook before. And aparently this cannot be done within the
        # constructor. An AttributeError exception would be the result.
        ioString = StringIO.StringIO()
        traceback.print_exception(self.type, self.value, self.traceback, None, ioString)
        tracebackText = ioString.getvalue()
        ioString.close()

        self.lblExcTraceback.set_text(tracebackText)

        # Show exception dialog
        self.dlgException.run()
        self.dlgException.hide()


    def on_btnExcSave__clicked(self, *data):
        '''
        Event handler which allows the user to store the traceback to a local
        file in order to send it in for debuging.

        NOTE: No matter how hard you try the mainwindow.MainWindow object
        will always be presented as a gtk.Window object here. Regardles if
        you pass its reference as a parameter, grab it from self.main.wnd
        or so. This means in effect there is no way at all to access the
        program's own main window methods. One cannot set a status message.
        '''
        # Ask user for file name
        fileName = kiwi.ui.dialogs.save(
            title        = _("Save Debug Information"),
            parent       = self.dlgException,
            current_name = "*.txt"
        )

        if not fileName:
            return

        fileObj = open(fileName, "w")
        traceback.print_exception(self.type, self.value, self.traceback, None, fileObj)
        fileObj.close()
