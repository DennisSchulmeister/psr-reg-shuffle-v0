#encoding=utf-8

# informationtab.py
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

This module provides a UI delegate class for the keyboard information page.
'''

# Public export of module content
__all__ = [
    "InformationTab"
]

# Import global modules
## NONE

# Import application modules
import const
import main
import appexceptions
import regbank.bankfile


# Class definition
class InformationTab:
    '''
    This is the UI delegate class for the keyboard information page.
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

        # Query regbank.Bankfile subclasses for information
        # and display it on the page
        self.wndMain.lblKeyboards.set_use_markup(True)

        try:
            classes = {}
            classNames = []

            for cls in regbank.bankfile.BankFile.getAllSubclasses():
                classes[cls.__name__] = cls
                classNames.append(cls.__name__)

            txt = ""
            classNames.sort()

            for className in classNames:
                cls = classes[className]

                maximumRegsPerBank = _("Registrations per bank: Up to %i") % (cls.maxReg)
                fileExtension      = _("Typical file extension: *.%s") % (cls.fileExt)
                supportedModels    = _("Models supported by this class:") + "\n\n"

                for name in cls.keyboardNames:
                    supportedModels += "\t» %s\n" % const.keyboardNameLong[name]

                if txt:
                    txt += "\n\n\n"

                txt += "<b>%(group)s</b>\n<i>%(descr)s</i>\n\n%(models)s\n%(maxReg)s\n%(fileExt)s" % {
                    "group":   cls.groupName,
                    "descr":   cls.information,
                    "models":  supportedModels,
                    "maxReg":  maximumRegsPerBank,
                    "fileExt": fileExtension,
                }

            txt += "\n"
            self.wndMain.lblKeyboards.set_markup(txt)
        except appexceptions.NoClassFound:
            self.wndMain.lblKeyboards = _("This installation comes with no keyboard support at all. In most cases this is not intended. Please check your installation for possible errors.")

