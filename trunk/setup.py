#!/usr/bin/env python
#encoding=utf-8

# setup.py
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

This is the install script. It employs distutils for system-wide installation
and packaging.

TODO
====

* Installation of gettext l8n files.
'''

# Provide global dummy _() function since we're not using gettext here.
# If this is left out importing modules from src won't work.
import __builtin__

if not hasattr(__builtin__, "_"):
     __builtin__.__dict__['_'] = lambda text: text


# Import modules
from distutils.core import setup
from glob import glob
import sys
import os

from src import const


# Package meta-data
NAME         = const.progname
VERSION      = const.version
DESCRIPTION  = const.description
AUTHOR       = const.author
AUTHOR_EMAIL = const.author_email
URL          = const.url

# See http://pypi.python.org/pypi?%3Aaction=list_classifiers for a
# complete list of available classifiers
CLASSIFIERS  = [
    "Development Status :: 4 - Beta",
    "Environment :: X11 Applications :: Gnome",
    "Environment :: X11 Applications :: GTK",
    "Intended Audience :: End Users/Desktop",
    "License :: OSI Approved :: GNU General Public License (GPL)",
    "Operating System :: POSIX",
    "Programming Language :: Python",
    "Topic :: Multimedia :: Sound/Audio :: Editors",

]


# Package dependencies
REQUIRES = [
    "gettext",
    "optparse",
    "pygtk (>=2.0)",
    "kiwi (>=1.9.19)"
]


# List of packages, package directories, scripts and additional data
SCRIPTS  = [
    "psrregshuffle"
]

PACKAGES    = [
    "psrregshuffle",
    "psrregshuffle.regbank",
    "psrregshuffle.regfile"
]

PACKAGE_DIR = {
    "psrregshuffle":         "src/",
    "psrregshuffle.regbank": "src/regbank",
    "psrregshuffle.regfile": "src/regfile"
}

DATA_SRC_DIR = os.path.join("data", "*")
DATA_DST_DIR = os.path.join("share", const.techname)
DATA_FILES   = [
    (DATA_DST_DIR, glob(DATA_SRC_DIR))
]


# Build man pages
# NOTE: Unfortunately there is no way to limit this to the distutils
# commands "build" or "install". So it gets executed every time the script
# runs.
cwd = os.getcwd()
os.chdir(os.path.join("doc", "man"))

import doc.man.make

os.chdir(cwd)


# Add man pages to list of data files
manBuildDir   = os.path.join("doc", "man", "build")
manInstallDir = os.path.join(sys.prefix, "share", "man")

for root, dirs, files in os.walk(manBuildDir):
    # Assemble list of source files per directory
    srcFiles = []

    for file in files:
        srcFiles.append(os.path.join(root, file))

    if not srcFiles:
        continue

    # Derive destination directory name
    dstDir = root.replace(manBuildDir, manInstallDir)

    # Append files to list of data files
    entry = (dstDir, srcFiles)
    DATA_FILES.append(entry)


# Build language dependant catalog files (l18n)
# NOTE: Unfortunately there is no way to limit this to the distutils
# commands "build" or "install". So it gets executed every time the script
# runs.
cwd = os.getcwd()
os.chdir("locale")

import l18n.import_translations

os.chdir(cwd)


# Add l8n files to list of data files
## TODO ##
print "INSTALLATION OF L8N FILES IS NOT YET SUPPORTED."


# Start setup-script
setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    classifiers=CLASSIFIERS,
    scripts=SCRIPTS,
    packages=PACKAGES,
    package_dir=PACKAGE_DIR,
    data_files=DATA_FILES,
    requires=REQUIRES
)
