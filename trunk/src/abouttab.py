#encoding=utf-8

# abouttab.py
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

This module provides a controller class for the "About" page. This function
used to be carried out by the MainWindow class. It has been moved here though
for the sake of shrinking the big MainWindow class.
'''

# Public export of module content
__all__ = [
    "AboutTab"
]


# Import global modules
import os.path

# Import application modules
import main
import const


# Class definition
class AboutTab:
    '''
    Simple controler class for running the "About" page.
    '''

    def __init__(self, wndMain):
        '''
        Default constructor. Sets the logo and text on the "About" page.
        '''
        # Initialize attributes
        self.main    = main.Main.getInstance()
        self.wndMain = wndMain

        # Set image and text of about pane
        logo_filename = os.path.join(self.main.dataDir, "logo_medium.png")
        self.wndMain.imgAbout.set_from_file(logo_filename)

        about_txt = "<big><big><big><b>%(progname)s %(version)s</b></big></big></big>\n<i>%(descr)s</i>\n\n%(licence)s" % \
        {
            "progname": const.progname,
            "version":  const.version,
            "descr":    const.description,
            "licence":  const.copyright_long,
            "thanks":   const.thanks,
        }

        self.wndMain.lblAbout.set_use_markup(True)
        self.wndMain.lblAbout.set_markup(about_txt)

        self.wndMain.linkAbout.set_label(const.url)
        self.wndMain.linkAbout.set_uri(const.url)

        self.wndMain.lblThanks.set_use_markup(True)
        self.wndMain.lblThanks.set_markup(const.thanks)
