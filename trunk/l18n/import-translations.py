#!/usr/bin/env python
#encoding=utf-8

# import-translations.py
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

This script builds man binary message catlogs from all translated *.po files of
the same directory. The external program msgfmt is used for that.

Please make sure the files are named correctly. Each input file must follow
the following pattern:

psrregshuffle.LOCALE.po

whereas LOCALE has to be substituted by the locale of the translation.
'''

# Import modules
import glob
import os
import os.path

# Print info message (mainly for setup.py)
print "BUILDING BINARY CATALOG FILES OF ALL TRANSLATIONS"

# Assemble list of input files
inputFiles = glob.glob("psrregshuffle.*.po")

# Remove sub-directories with old catalogs
for root, dirs, files in os.walk("build", topdown=False):
    for name in files:
        os.remove(os.path.join(root, name))
    for name in dirs:
        os.rmdir(os.path.join(root, name))

# Build catalog files from input files
for filename in inputFiles:
    # Extract locale name
    filenameParts  = filename.split(".")
    localeName     = filenameParts[1]

    # Create output file name
    outputDirName  = os.path.join("build", localeName, "LC_MESSAGES")
    outputFilename = "%s.mo" % (filenameParts[0])
    outputFilename = os.path.join(outputDirName, outputFilename)

    # Create locale specific output directory
    try:
        os.makedirs(outputDirName, 0755)
    except:
        pass

    # Build catalog file
    command = "msgfmt --check --output-file=%s %s" % (outputFilename, filename)
    os.system(command)
