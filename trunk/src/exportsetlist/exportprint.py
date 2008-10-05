#encoding=utf-8

# exportsetlisttab.py
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

This module provides a class for printing the content a setlist.
'''

# Public export of module content
__all__ = [
    "ExportPrint",
]


# Import global modules
import kiwi.ui.dialogs
import gtk
import pango
import time

# Import application modules
import appexceptions
import exportbase
from .. import const


# Class for setlist printing
class ExportPrint(exportbase.ExportBase):
    '''
    This class allows to print the contents of a list of BankFiles.
    '''

    # Static attributes........................................................

    displayName = _("_Print Setlist")


    # Export routines..........................................................

    def getSuccessMessage(self):
        '''
        Returns a success message which can be shown after successful export.
        '''
        return self.successMsg


    def prepare(self):
        '''
        Called before the export begins. Can be used to ask user for filename
        etc. Needs to throw appexceptions.Cancel if the user chooses to abort.
        '''
        # Initiliaize object
        self.successMsg = ""
        self.pages = 0

        # Initialize bank list
        self.banks = []
        self.currentBank = ""


    def addCurrentBank(self):
        '''
        Adds the current bank to the bank list.
        '''
        if self.currentBank:
            self.currentBank += "\n"             # One blank line between banks
            self.banks.append(self.currentBank)

    def onNewBank(self, setlistEntry):
        '''
        Called each time a new bank starts. Used to export the bank's name.
        Takes a printsetlisttab.SetlistEntry object.
        '''
        # Add previous bank to bank list
        self.addCurrentBank()

        # Initialize new bank heading
        bankName = setlistEntry.shortname
        bankName = bankName.replace("<", "&lt;")
        bankName = bankName.replace(">", "&gt;")

        self.currentBank = "<big><b>%s</b></big>\n" % (bankName)
        self.currentBank = self.currentBank.replace("&", "&amp;")

        # Reset registration counter
        self.regCount = 0


    def onNewRegistration(self, regObj):
        '''
        Called for each registration within a bank. Used to export the
        registration's data. Takes Registration object.
        '''
        # Calculate registration name and number
        if regObj:
            regName = regObj.stripName(regObj.getName())
            regName = regName.replace("&", "&amp;")
            regName = regName.replace("<", "&lt;")
            regName = regName.replace(">", "&gt;")
        else:
            regName = const.REG_NAME_EMPTY

        self.regCount += 1

        # Add registration to current bank
        self.currentBank += "\t<b>[%i]</b> %s\n" % (self.regCount, regName)


    def finish(self):
        '''
        Called after exporting all bank files. Used to close files, start
        printing etc.
        '''
        # Add final bank to bank list
        self.addCurrentBank()

        # Initialize print job
        printOperation = gtk.PrintOperation()

        # Connect to signals
        printOperation.connect("begin-print", self.onBeginPrint)
        printOperation.connect("draw-page", self.onDrawPage)

        # Show print dialog and start printing
        result = printOperation.run(
            action = gtk.PRINT_OPERATION_ACTION_PRINT_DIALOG,
            parent = self.wndMain.wndMain
        )

        if result == gtk.PRINT_OPERATION_RESULT_CANCEL:
            self.successMsg = const.msg["setlist-print-cnc"]
        elif result == gtk.PRINT_OPERATION_RESULT_ERROR:
            self.successMsg = const.msg["setlist-print-err"] % (printOperation.get_error())
        else:
            self.successMsg = const.msg["setlist-print-ok"] % (self.printName)


    # Print methods............................................................

    def onBeginPrint(self, printOperation, printContext):
        '''
        Event handler for begin of print operation. Paginates output.
        Automaticaly called by a gtk.PrintOperation object.
        '''
        # NOTE: Need to catch all exceptions and leave method in order to not
        # get stuck in an infinite-loop.
        try:
            # Set job name
            printOperation.set_job_name(const.msg["printjob-name"] % (self.printName))

            # Retrieve objects and information
            self.cairoContext = printContext.get_cairo_context()
            self.width  = int(printContext.get_width())
            self.height = int(printContext.get_height())

            # Prepare pango layouts for page header
            fontDescr = pango.FontDescription("Sans 14")

            self.layoutL = printContext.create_pango_layout()
            self.layoutL.set_font_description(fontDescr)
            self.layoutL.set_width(self.width * pango.SCALE)
            self.layoutL.set_alignment(pango.ALIGN_LEFT)
            self.layoutL.set_markup("dummy\ndummy\n\n")

            self.layoutR = printContext.create_pango_layout()
            self.layoutR.set_font_description(fontDescr)
            self.layoutR.set_width(self.width * pango.SCALE)
            self.layoutR.set_alignment(pango.ALIGN_RIGHT)
            self.layoutR.set_markup("dummy\ndummy\n\n")

            # Prepare pango layouts for bank content
            self.bankLayouts = []
            fontDescr = pango.FontDescription("Sans 12")

            nPages = 1
            self.headerWidth, self.headerHeight = self.layoutL.get_size()
            self.headerWidth  /= pango.SCALE
            self.headerHeight /= pango.SCALE

            currentHeight = self.headerHeight

            for bank in self.banks:
                # Create pango layout for bank content
                layout = printContext.create_pango_layout()

                layout.set_font_description(fontDescr)
                layout.set_width(self.width * pango.SCALE)
                layout.set_alignment(pango.ALIGN_LEFT)
                layout.set_markup(bank)

                self.bankLayouts.append(layout)

                # Try to add this bank to current page
                textWidth, textHeight = layout.get_size()
                textWidth  /= pango.SCALE
                textHeight /= pango.SCALE

                currentHeight += textHeight

                if currentHeight > self.height:
                    # Start new page if necessary
                    # Add header as well as bank which didn't fit on previous page
                    nPages += 1
                    currentHeight = self.headerHeight + textHeight

            printOperation.set_n_pages(nPages)
            self.pages = nPages
        except:
            return True


    def onDrawPage(self, printOperation, printContext, pageNr):
        '''
        Event handler to print a single page given by the page number.
        Automaticaly called by a gtk.PrintOperation object.
        '''
        # NOTE: Need to catch all exceptions and leave method in order to not
        # get stuck in an infinite-loop.
        try:
            # Render page header
            self.printHeader(printOperation, printContext, pageNr)

            # Get cairo context
            cairoContext = printContext.get_cairo_context()
            cairoContext.set_source_rgb(0, 0, 0)

            # Render bank content
            textY  = self.headerHeight
            height = self.headerHeight

            while True:
                try:
                    layout = self.bankLayouts[0]
                except IndexError:
                    break

                textY  = height

                textWidth, textHeight = layout.get_size()
                textWidth  /= pango.SCALE
                textHeight /= pango.SCALE

                height += textHeight

                if height < self.height:
                    cairoContext.move_to(0, textY)
                    cairoContext.show_layout(layout)

                    self.bankLayouts = self.bankLayouts[1:]
                else:
                    break
        except:
            return True


    def printHeader(self, printOperation, printContext, pageNr):
        '''
        Called by onDrawPage event handler to draw the page header.
        '''
        # Get cairo context
        cairoContext = printContext.get_cairo_context()

        # Calculate header text
        mainText = " " + const.msg["setlist-page-head"] % {
            "name":  self.printName,
            "page":  pageNr + 1,
            "pages": self.pages,
        }

        mainText = mainText.replace("&", "&amp;")
        mainText = mainText.replace("\n", "\n ")      # Distance to border line

        # Draw border
        self.layoutL.set_markup("%s\n" % (mainText))
        borderWidth = printContext.get_width()
        dummy, borderHeight = self.layoutL.get_size()
        borderHeight = borderHeight / pango.SCALE

        cairoContext.rectangle(0, 0, borderWidth, borderHeight)

        cairoContext.set_source_rgb(0, 0, 0)
        cairoContext.set_line_width(1)
        cairoContext.stroke_preserve()

        cairoContext.set_source_rgb(0.75, 0.75, 0.75)
        cairoContext.fill()

        # Draw header text
        cairoContext.set_source_rgb(0, 0, 0)

        self.layoutL.set_markup(mainText)
        self.layoutR.set_markup("\n%s " % (time.strftime("%c")))

        textWidth, textHeight = self.layoutL.get_size()
        textWidth  /= pango.SCALE
        textHeight /= pango.SCALE
        textY = (borderHeight - textHeight) / 2

        cairoContext.move_to(0, textY)
        cairoContext.show_layout(self.layoutL)

        cairoContext.move_to(0, textY)
        cairoContext.show_layout(self.layoutR)
