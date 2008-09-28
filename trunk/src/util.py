#encoding=utf-8

# util.py
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

This module contains utility functions which cannot be in main singleton
object. Unfortunatly importing ..main from a sub-package almost always leads
to circular impors which crash the application.
'''

# Import global modules
import os.path
import gtk.glade
import gettext
import locale


# Import application modules
import appexceptions
import regfile


# Define functions
def initGettext(domainName, localeDir):
    '''
    This function kick-starts internationalization by initializing
    gettext. As a result the function _("...") will be installed into
    the global builtin dictionary.
    '''
    # Set locale for glade UI
    gtk.glade.bindtextdomain(domainName, localeDir)
    gtk.glade.textdomain(domainName)

    # Determine available languages on the system
    lc, encoding = locale.getdefaultlocale()
    envLanguage  = os.environ.get("LANGUAGE", None)

    if lc:
        languages = [lc]
    else:
        languages = []

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


def getFileObject(filename="", file=None):
    '''
    This function can either take a filename or a file object or both.
    In any case it returns a file object which can be used for read
    the given file.

    If only file is given it gets straight returned. If filename is given
    a new file object will be created and be returen. If both are given
    a new file object will be created, too.

    If none is given appexceptions.NoFileGiven gets raised.
    '''
    # Return file object if given
    if file:
        return file

    # Try to open a new file
    if filename:
        return open(filename, "rb")

    # Throw exception
    raise appexceptions.NoFileGiven()


def calculateFileNameFromRegName(name, workDir):
    '''
    Calculates a unique file name which also contains the name of the
    registration. The first iteration tries to simply add a regfile extension.
    Than an appended number gets incremented with each iteration until a
    unique name has been found.
    '''
    nr = 0
    fileName = "%s.%s" % (name, regfile.extension)
    fileName = os.path.join(workDir, fileName)

    while os.path.exists(fileName):
        nr += 1
        fileName = "%s (%i).%s" % (name, nr, regfile.extension)
        fileName = os.path.join(workDir, fileName)

    return fileName


def stripNameYamaha(name="", fileExt=""):
    '''
    This function strips object names as they are used by several Yamaha
    keyboard models. It does so by removing the file extension and the
    icon descriptor. (Typical name string: "xyz.S136.reg").

    This method is not meant for direct usage. It's just there to prevent
    duplicate implementation by several Yamaha related BankFile and
    Registration subclasses.

    Don't use this method directly. Use the regbank.* classes instead.
    '''
    # Strip extension
    nameUpper    = name.upper()
    fileExtUpper = "." + fileExt.upper()

    if fileExt:
        if nameUpper.endswith(fileExtUpper):
            name = name[: - len(fileExtUpper)]
            nameUpper = name.upper()

    # Strip icon name
    if nameUpper[-5:-3] == ".S":
        name = name[:-5]
        nameUpper = name.upper()

    return name
