#! /usr/bin/env python
#encoding=utf-8

# extract-all-strings.py
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
Purpose
=======

This script uses xgettext for extracting all translatable strings from
all source and glade files. Output is stored to psrregshuffle.po.

If run with the command line option "--clean" (or "-c" for short) a cleanup
will be performed where all generated files will be removed.
'''

# Import modules
import os
import os.path
import glob
import sys


# Define parameters
# ATTENTION: Command line parameters of xgettextArgs must be shell-like quoted.
outputDirectory = os.getcwd()
outputFilename  = os.path.join(outputDirectory, "psrregshuffle.po")
xgettextArgs    = "--join-existing --add-location --width=%(width)s --sort-output --copyright-holder=%(copyright)s --package-name=%(package)s --package-version=%(version)s --msgid-bugs-address=%(bugmail)s --output=%(outputFilename)s" \
% {
    "package":       "psrregshuffle",
    "version":       "0.1",
    "copyright":     "Dennis\ Schulmeister",
    "bugmail":       "dennis\ -at-\ ncc-1701a.homelinux.net",
    "width":         "80",
    "outputFilename": outputFilename,
}
knownFiletypes  = ["*.py", "*.glade"]



# Define cleanup function
def cleanup_build_files():
    '''
    This function removes all possibly generated files. Its meant for cleanup
    either at the users request or before building new files.
    '''
    global outputFilename
    os.remove(outputFilename)


# Define processing function
def process_dir(dirName, recursive):
    '''
    This functions starts xgettext for all python and glade files within the
    given directory. The second parameter decides whether the function calls
    itself recursively for all sub-directories.
    '''
    # Bring in global script parameters
    global outputDirectory, outputFilename, xgettextArgs, knownFiletypes

    # Extract translateable strings
    dirName = os.path.abspath(dirName)
    print "#### PROCESSING %s" % dirName

    for filetype in knownFiletypes:
        pattern = os.path.join(dirName, filetype)

        if not glob.glob(pattern):
            continue

        command = "xgettext %s %s" % (xgettextArgs, pattern)
        os.system(command)

    # Recurse into sub-directories
    if not recursive:
        return

    for root, dirs, files in os.walk(dirName, topdown=True):
        for dir in dirs:
            # Skip dot-directories and let os.walk() know it
            if dir[0] == ".":
                dirs.remove(dir)
                continue

            process_dir(os.path.join(root, dir), recursive=True)



# Check command line options
for arg in sys.argv[1:]:
    if arg == "--clean" or arg == "-c":
        # Cleanup request detected
        print "CLEANING UP"
        cleanup_build_files()
        sys.exit()


## Clear existing output file
#try:
#    file = open(outputFilename, "w")
#    file.close()
#except:
#    pass


# Process files of top-directory
process_dir("..", recursive=False)


# Process files of data/-directory
process_dir(os.path.join("..", "data"), recursive=True)


# Process files of src/-directory
process_dir(os.path.join("..", "src"), recursive=True)
