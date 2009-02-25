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

# Declare constant values
#
# ATTENTION: When program name (or version number) changes don't forget to
# change ../psrregshuffle -> domain_name so that a new localization domain will
# be established!! Also don't forget to adopt ../l18n/extract_all_strings.py
# by adjusting the parameters for xgettext.

progname       = "PSR Registration Shuffler"
shortname      = "psrregshuffle"
version        = "0.3"
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

thanks = """%(intro)s

<b>Heiko Plate</b>
%(Heiko Plate)s

<b>Jørgen Sørensen</b>
%(Jørgen Sørensen)s

<b>Michael P. Bedesem</b>
%(Michael P. Bedesem)s

<b>Leroy Luc</b>
%(Leroy Luc)s

<b>Jim Wincell</b>
%(Jim Wincell)s

<b>Brian Haylett</b>
%(Brian Haylett)s

<b>Tom G</b>
%(Tom G)s

<b>Ray from downunder</b>
%(Ray from downunder)s

<b>Mike Comley</b>
%(Mike Comley)s

<b>Herbert Mauderer</b>
%(Herbert Mauderer)s

<b>Norm Ruttle</b>
%(Norm Ruttle)s

<b>Alan Paganelli</b>
%(Alan Paganelli)s

<b>Kim Winther</b>
%(Kim Winther)s

<b>Claudio Bizzarri</b>
%(Claudio Bizzarri)s

<b>%(internet_name)s</b>
%(The Internet)s

<b>%(anyone_else_name)s</b>
%(Anyone else)s""" % {
    "intro":                _("Special thanks go to the following people. Without their help this program would still\nsupport Yamaha PSR-2000 and Linux only."),
    "Heiko Plate":          _("For his documentation of the Yamaha PSR-2000 registration file format.\nWithout it I would have never started to write this program."),
    "Jørgen Sørensen":      _("For writing excellent music related software which encouraged me to try the same."),
    "Michael P. Bedesem":   _("For all his music related software. Also for providing Yamaha Tyros 3 test data."),
    "Leroy Luc":            _("For trying to run the program in Windows when there hasn't been\na dedicated package yet."),
    "Jim Wincell":          _("For being one of the first who tried out the Windows package."),
    "Brian Haylett":        _("For answering questions on the different keyboard models."),
    "Tom G":                _("For providing Yamaha Tyros 2 registration files."),
    "Ray from downunder":   _("For providing Yamaha Tyros 1 registration files."),
    "Mike Comley":          _("For providing Yamaha S900 registration files."),
    "Herbert Mauderer":     _("For providing Yamaha S700 registration files."),
    "Norm Ruttle":          _("For providing Yamaha PSR-3000 registration files."),
    "Alan Paganelli":       _("For providing Yamaha Tyros 1 registration files."),
    "Kim Winther":          _("For providing Yamaha Tyros 3 registration files."),
    "Claudio Bizzarri":     _("For trying to run this program on Ubuntu GNU/Linux 7.10 and reporting about a\nmissing method in the kiwi library.\n\nAlso for offering his help with the Italian translation."),
    "internet_name":        _("The nice folks who hang around the Internet"),
    "The Internet":         _("Including members of the Yamaha-psr-Yahoogroups,\nSVPWorld.com and many more."),
    "anyone_else_name":     _("Anyone whom I left out"),
    "Anyone else":          _("You know who you are. Drop me a message  if you want\nand I'll add your name to the list."),
}

# Displayed name for empty registrations
REG_NAME_EMPTY = _("### EMPTY ###")


# Filter modes
FILTER_UNDEFINED  = ""
FILTER_NONE       = "NONE"
FILTER_COMPATIBLE = "COMP"
FILTER_MODEL      = "MODEL"


# Sort modes
SORT_BY_NAME_ASC  = "NAME ASC"
SORT_BY_NAME_DESC = "NAME DESC"
SORT_RANDOM       = "RAND"


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
YAMAHA_TYROS3  = "YAMAHA TYROS3"
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
    YAMAHA_TYROS3:  "Yamaha Tyros 3",
    YAMAHA_S500:    "Yamaha PSR-S500",
    YAMAHA_S700:    "Yamaha PSR-S700",
    YAMAHA_S900:    "Yamaha PSR-S900",
}


# Constants with message texts
msg = {
    "ready":              _("Ready."),
    "invalid-key-name":   _("ATTENTION: Please choose a keyboard model first."),
    "changed-dir":        _("Changed directory to '%s'."),
    "browser-opened":     _("Successfully opened web browser."),
    "browser-not-opened": _("Unable to launch web browser."),
    "bank-open-success":  _("Successfully opened '%(filename)s' registration bank file."),
    "bank-add-success":   _("Successfully added '%(filename)s' to the list."),
    "nothing-imported":   _("Nothing imported."),
    "import-ok":          _("Successfully imported %i registrations."),
    "clear-ok":           _("Cleared new registration bank."),
    "moved-one-up":       _("Moved '%s' up one position."),
    "moved-one-down":     _("Moved '%s' down one position."),
    "bank-save-ok":       _("Saved registration bank to '%s'."),
    "incompatible-keys":  _("ATTENTION: %(dstName)s cannot read registrations from %(srcName)s."),
    "max-allowed-regs":   _("ATTENTION: A bank file for this instrument can only hold up to %i registrations."),
    "added-to-bank":      _("Added '%s' to new bank."),
    "removed-from-bank":  _("Removed '%s' from new bank."),
    "n-banks-created":    _("Successfully created %i registration banks."),
    "setlist-export-ok":  _("Successfully exported setlist to '%s'."),
    "setlist-print-ok":   _("Started print job: '%s'"),
    "setlist-print-err":  _("PRINT ERROR: %s"),
    "setlist-print-cnc":  _("Print operation canceled."),
    "printjob-name":      _("PSR setlist: %s"),
    "setlist-page-head":  _("<b>%(name)s</b>\nPage %(page)s of %(pages)s"),
}
