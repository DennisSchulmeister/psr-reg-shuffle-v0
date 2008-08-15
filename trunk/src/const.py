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
version        = "0.1"
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

<b>Leroy Luc</b>
For trying to run the program in Windows when there hasn't been a dedicated
package yet

<b>Jim Wincell</b>
For being one of the first who tried out the Windows package

<b>Bob Gelman</b>
For spreading the word and hiring volunteers who'd provide test data

<b>Brian Haylett</b>
For helping Tom to manage his Yamaha Tyros 2 keyboard and for answering questions

<b>Tom G</b>
For providing Yamaha Tyros 2 registraion files and for being a friend on Yahoogroups

<b>Ray from downunder</b>
For providing Yamaha Tyros 1 registration files

<b>Jeff from the Netherlands</b>
For being a friend on yamaha-psr-Yahoogroups and for spreading the word there

<b>Hennie van Rooyen</b>
For alerting the community on a possible threat from the Windows package

<b>Michael P. Bedesem</b>
For being a friend on Yahoogroups and for encouraging me to continue working
on the program

<b>Mike Comley</b>
For providing Yamaha S900 registration files

<b>Norm Ruttle</b>
For providing Yamaha PSR-3000 registration files

<b>Jørgen Sørensen</b>
For writing excelent music related software which encourged me to try the same

<b>Alan Paganelli</b>
For providing Yamaha Tyros 1 registration files

<b>Claudio Bizzarri</b>
For trying to run this program on Ubuntu GNU/Linux 7.10 and reporting about a
missing method in the kiwi library.

Also for offering his help with the Italian translation.

<b>The nice folks who hang around the Internet</b>
Including members of the Yamaha-psr-Yahoogroups, the German Yamaha music forum,
SVPWorld.com and many more.

Also including all those programmers who spend their time in the Usenet,
mailing lists and blogs etc.

All members and friends of free and open-sourced software. Without you guys
not only this program but many many more would have never been possible.

<b>Anyone whom I left out</b>
Sorry, if I missed you here. Just drop me a message if you want and I'll add
your name to the list.
""")

# Constants with technical short names for keyboard models
ALL_MODELS     = ""
UNKNOWN_MODEL  = "UNKNOWN"
YAMAHA_PSR2000 = "YAMAHA PSR2000"
YAMAHA_PSR3000 = "YAMAHA PSR3000"
YAMAHA_TYROS1  = "YAMAHA TYROS1"
YAMAHA_TYROS2  = "YAMAHA TYROS2"
YAMAHA_S900    = "YAMAHA S900"

# Dictionary with user-friendly product names. (Not all translateable)
keyboardNameLong = {
    ALL_MODELS:     _("All models"),
    UNKNOWN_MODEL:  _("Unknown model"),
    YAMAHA_PSR2000: "Yamaha PSR-2000",
    YAMAHA_PSR3000: "Yamaha PSR-3000",
    YAMAHA_TYROS1:  "Yamaha Tyros 1",
    YAMAHA_TYROS2:  "Yamaha Tyros 2",
    YAMAHA_S900:    "Yamaha S900",
}
