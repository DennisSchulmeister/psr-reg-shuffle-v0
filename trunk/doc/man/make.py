#!/usr/bin/env python
#encoding=utf-8

# make.py
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

This script builds man pages from all *.txt files of the same directory.
The external program help2man is used for creating the man pages. This
program works by taking the --version and --help output of the application
plus some additional data from the text files.

Please make sure the files are named correctly. Each input file must follow
the following pattern:

psrregshuffle.LOCALE.txt

whereas LOCALE has to be substituted by the locale for which the man page
has to be built.
'''

# Import modules
import glob
import os
import os.path

# Print info message (mainly for setup.py)
print "BUILDING MAN PAGES"

# Assemble list of input files
inputFiles = glob.glob("psrregshuffle.*.txt")

# Remove sub-directories with old man page versions
for root, dirs, files in os.walk("build", topdown=False):
    for name in files:
        os.remove(os.path.join(root, name))
    for name in dirs:
        os.rmdir(os.path.join(root, name))

# Create man pages from input files
for filename in inputFiles:
    # Extract locale name
    filenameParts  = filename.split(".")
    localeName     = filenameParts[1]

    # Create output file name
    outputDirName  = os.path.join("build", localeName, "man1")
    outputFilename = "%s.1.gz" % (filenameParts[0])
    outputFilename = os.path.join(outputDirName, outputFilename)

    # Create locale specific output directory
    try:
        os.makedirs(outputDirName, 0755)
    except:
        pass

    # Build man page
    command = "help2man --locale=%s --include=%s --output=%s --no-info ../../start-dev-version" % (localeName, filename, outputFilename)
    os.system(command)
