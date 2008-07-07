#!/usr/bin/python
#encoding=utf-8

# psr-reg-shuffle.py
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

This script starts the system-wide installed version of the application.
'''

# Import global modules
import gettext
import sys
import os

# Initialize l8n support
domain_name = "psr-reg-shuffle-0.1"
locale_dir     = os.path.join(sys.prefix, domain_name, "locale")

gettext.install(domain_name, locale_dir, unicode=1)


# Start application
import psrregshuffle.main
psrregshuffle.main.run()
