#encoding=utf-8

# const.py
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

This module declares application wide constants.
'''

# Public export of module content
__all__ = [
    "progname",
    "shortname",
    "version",
    "techname",
    "licence",
    "description",
    "author",
    "author_email",
    "url",
    "copyright",
    "copyright_long",
    "version_string",
]


# Import modules
import sys
import os.path

# Declare constant values
#
# ATTENTION: When program name (or version number) changes don't forget to
# change ../psrregshuffle -> domain_name so that a new localization domain will
# be established!! Also don't forget to adopt ../l18n/extract_all_strings.py
# by adjusting the parameters for xgettext.

progname       = "PSR Registration Shuffler"
shortname      = "psr-reg-shuffle"
version        = "0.2"
techname       = "%s-%s" % (shortname, version)
licence        = "GNU General Public Licence 3"
description    = _("A program for organizing PSR registration bank files")
author         = "Dennis Schulmeister"
author_email   = "dennis -at- ncc-1701a.homelinux.net"
url            = "http://www.psrregshuffle.de"

copyright      = "Copyright (C) 2008 %s" % (author)
copyright_long = _("""%s

This is free software; you can redistribute it and/or modify it under the terms
of the GNU General Public License as published by the Free Software Foundation;
either version 3 of the License, or (at your option) any later version.

The software is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE.  See the GNU General Public License for more details.
""") % (copyright)

version_string = _("%(progname)s %(version)s\n\n%(copyright_long)s\nWritten by %(author)s <%(author_email)s>") % \
{
    "progname":       progname,
    "version":        version,
    "copyright_long": copyright_long,
    "author":         author,
    "author_email":   author_email
}

thanks = _("""Special thanks go to the following people. Without their help this program
would still support Yamaha PSR-2000 and Linux only.

<b>Heiko Plate</b>
For his documentation of the Yamaha PSR-2000 registration file format. Without
it I would have never started to write this program

<b>Jørgen Sørensen</b>
For writing excelent music related software which encourged me to try the same

<b>Michael P. Bedesem</b>
For all his music related software

<b>Leroy Luc</b>
For trying to run the program in Windows when there hasn't been a dedicated
package yet

<b>Jim Wincell</b>
For being one of the first who tried out the Windows package

<b>Brian Haylett</b>
For answering questions on the different keyboard models

<b>Tom G</b>
For providing Yamaha Tyros 2 registraion files

<b>Ray from downunder</b>
For providing Yamaha Tyros 1 registration files

<b>Mike Comley</b>
For providing Yamaha S900 registration files

<b>Norm Ruttle</b>
For providing Yamaha PSR-3000 registration files

<b>Alan Paganelli</b>
For providing Yamaha Tyros 1 registration files

<b>Claudio Bizzarri</b>
For trying to run this program on Ubuntu GNU/Linux 7.10 and reporting about a
missing method in the kiwi library.

Also for offering his help with the Italian translation.

<b>The nice folks who hang around the Internet</b>
Including members of the Yamaha-psr-Yahoogroups, the German Yamaha music forum,
SVPWorld.com and many more.

<b>Anyone whom I left out</b>
You know who you are. Drop me a message if you want and I'll add your name to
the list.
""")

# Constants with technical short names for keyboard models
ALL_MODELS     = ""
UNKNOWN_MODEL  = "UNKNOWN"
YAMAHA_PSR740  = "YAMAHA PSR740"
YAMAHA_PSR1000 = "YAMAHA PSR1000"
YAMAHA_PSR1100 = "YAMAHA PSR1100"
YAMAHA_PSR2000 = "YAMAHA PSR2000"
YAMAHA_PSR2100 = "YAMAHA PSR2100"
YAMAHA_PSR3000 = "YAMAHA PSR3000"
YAMAHA_PSR8000 = "YAMAHA PSR8000"
YAMAHA_PSR9000 = "YAMAHA PSR9000"
YAMAHA_TYROS1  = "YAMAHA TYROS1"
YAMAHA_TYROS2  = "YAMAHA TYROS2"
YAMAHA_S500    = "YAMAHA S500"
YAMAHA_S700    = "YAMAHA S700"
YAMAHA_S900    = "YAMAHA S900"

# Dictionary with user-friendly product names. (Not all translateable)
keyboardNameLong = {
    ALL_MODELS:     _("All models"),
    UNKNOWN_MODEL:  _("Unknown model"),
    YAMAHA_PSR740:  "Yamaha PSR-740",
    YAMAHA_PSR1000: "Yamaha PSR-1000",
    YAMAHA_PSR1100: "Yamaha PSR-1100",
    YAMAHA_PSR2000: "Yamaha PSR-2000",
    YAMAHA_PSR2100: "Yamaha PSR-2100",
    YAMAHA_PSR3000: "Yamaha PSR-3000",
    YAMAHA_PSR8000: "Yamaha PSR-8000",
    YAMAHA_PSR9000: "Yamaha PSR-9000 / 9000pro",
    YAMAHA_TYROS1:  "Yamaha Tyros 1",
    YAMAHA_TYROS2:  "Yamaha Tyros 2",
    YAMAHA_S500:    "Yamaha PSR-S500",
    YAMAHA_S700:    "Yamaha PSR-S700",
    YAMAHA_S900:    "Yamaha PSR-S900",
}


# Constants with message texts
msg = {
    "ready":              _("Ready."),
    "invalid-key-name":   _("ATTENTION: Please choose a keyboard model first."),
    "changed-dir":        _("Changed directory to %s."),
    "browser-opened":     _("Sucessfully opened web browser."),
    "browser-not-opened": _("Unable to launch web browser."),
    "bank-open-success":  _("Successfully opened %(filename)s registration bank file."),
    "nothing-imported":   _("Nothing imported."),
    "import-ok":          _("Nothing imported."),
    "clear-ok":           _("Cleared new registration bank."),
    "moved-one-up":       _("Moved '%s' up one position."),
    "moved-one-down":     _("Moved '%s' down one position."),
    "bank-save-ok":       _("Saved registration bank to '%s'."),
    "incompatible-keys":  _("ATTENTION: %(dstName)s cannot read registrations from %(srcName)s."),
    "max-allowed-regs":   _("ATTENTION: A bank file for this instrument can only hold up to %i registrations."),
    "added-to-bank":      _("Added '%s' to new bank."),
    "removed-from-bank":  _("Removed '%s' from new bank."),
}
