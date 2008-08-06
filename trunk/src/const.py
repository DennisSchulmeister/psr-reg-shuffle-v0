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


# Constants with technical short names for keyboard models
ALL_MODELS     = ""
YAMAHA_PSR2000 = "YAMAHA PSR2000"

# Dictionary with user-friendly product names. (Not translateable)
keyboardNameLong = {
    ALL_MODELS:     _("All models"),
    YAMAHA_PSR2000: "Yamaha PSR-2000"
}
