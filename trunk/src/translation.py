#encoding=utf-8

# translation.py
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

This module contains utility functions which enable translation of the
application to other languages. This means neither this module nor any
imported module contains translatable strings at all because the functions
contained here are meant to kick-start translation.

Two functions are defined here:

"init" takes a domain name (usually the name of the application) and a
locale dir. It then finds a suitable translation and registers the global
"_"-function in the __builtin__ dictionary.

"initDummy" however takes no argument. It is meant for development scripts
which need to import some of the code modules. It registers a global
"_"-function, too. But this function won't perfrom any translation. Instead
it will just return the given string.
'''

# Import global modules
import __builtin__
import gtk.glade
import gettext
import locale
import os

# Import application modules
# NONE YET


# Define functions
def init(domainName, localeDir):
    '''
    This function kick-starts internationalization by initializing
    gettext. As a result the function _("...") will be installed into
    the global builtin dictionary.
    '''
    # Set locale for glade UI
    gtk.glade.bindtextdomain(domainName, localeDir)
    gtk.glade.textdomain(domainName)

    # Determine available languages on the system
    # NOTE: Generating man pages for locale "en" only (instead of "en_GB" or
    # "en_US" ...) results in a locale "en_EN" which makes the below function
    # call raise an Error (Unknown locale) exception. If the exception won't
    # be catched (or the man page locale changed) it'll be impossible to create
    # man pages,
    try:
        lc, encoding = locale.getdefaultlocale()

        if lc:
            languages = [lc]
        else:
            languages = []
    except Error:
        languages = []

    envLanguage  = os.environ.get("LANGUAGE", None)

    if envLanguage:
        languages += envLanguage.split(":")

    # Install global _-function
    # NOTE: gettext.install(...) would be a nice one-liner if it worked on
    # Windows, too. Unfortunately it seems to work on *nix only. When used
    # on Windows no string would be translated at all.
    translation = gettext.translation(
        domainName,
        localeDir,
        languages = languages,
        fallback  = True
    )

    __builtin__.__dict__["_"] = translation.gettext


def initDummy():
    '''
    This function is meant for development scripts. It installs a global
    "_"-function which just returns the given string without performing any
    translation.
    '''
    __builtin__.__dict__["_"] = lambda txt: txt
