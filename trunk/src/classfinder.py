#encoding=utf-8

# classfinder.py
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

Most classes of the regbank package are derived from the Registration or
the RegBank class whereas both super-classes merely define a common API and
a basic set of common routines. Useful functionality comes from the sub-
classes which mostly implement keyboard model dependant specialities.

In order to provide hard coupling to those model specific classes and in order
to easy deployment of them a ClassFinder object is used in order to detect
a suiting class for a given keyboard model or bank file during runtime.

The class ClassFinder as declared in this module is not meant to be used by
application parts which wish to find a model specific handler class directly.
Instead the aforementioned super-classes (RegBank and Registraion) provide
static class methods of the name getClassFor... as a very high-level interface.
So basically they provide a class method which searches one of their own
sub-classes suiatbale for the task at hand.

Internaly those methods make use of a ClassFinder object which performs the
real search. Besides avoiding superfolous implementations of the same algorithm
that object makes use of a simple caching strategy which asures that the class
tree won't get browsed more than absolutely necessary. This should provide a
significatant speedup as in some cases (e.g. when scanning the registration
files of the work (data) directory) the very same search which also includes
disk access would be conducted many times.
'''

# Import global modules
import os
import os.path
import types
import glob
import sys

# Import application modules
import appexceptions


# Define class
class ClassFinder:
    '''
    A ClassFinder object searches all sub-classes of a given class within
    a given package and calls a pre-definded test method in order to find a
    class which passes the test. Searches get remembered by their hash value
    within a dictionary in order to avoind unnecessary package scanning.
    '''

    def __init__(self, superClass, classes, testMethName, hashMethName):
        '''
        Constructor. Takes the following arguments:

        ============== ========================================================
        Argument       Description
        ============== ========================================================
        superClass     Class object which marks beginning of the search tree.
        classes        List of scaned class objects
        testMethName   Name of the test method. (Only one parameter)
        hashMethName   Hash method. Like test method but returns a hash value.
        ============== ========================================================
        '''

        # Check if superclass is a class object
        if not superClass or not isinstance(superClass, (type, types.ClassType)):
            raise NoClassObject(superClass)

        # Store parameters
        self.superClass   = superClass
        self.classes      = classes
        self.testMethName = testMethName
        self.hashMeth     = getattr(superClass, hashMethName)
        self.cache        = {}


    def lookupCache(self, search):
        '''
        This method uses the given hash method in order to lookup previous
        search results in the internal cache. Positive lookups return a list of
        class objects. Raises appexceptions.NoClassFound otherwise.
        '''
        # Lookup search result
        try:
            hashValue  = self.hashMeth(search)
            return self.cache[hashValue]
        except KeyError:
            raise appexceptions.NoClassFound()


    def appendCache(self, search, foundClasses):
        '''
        This method uses the given hash method in order to store a search
        result into the internal cache.
        '''
        # Store search result
        hashValue = self.hashMeth(search)
        self.cache[hashValue] = foundClasses


    def scanClasses(self, search):
        '''
        This method scans every sub-class within the given package and
        runs its test method. If one method returns a positive value (True)
        its class will be returned. Otherwise appexceptions.NoClassFound will be
        raised.
        '''
        # Visit each class and query
        foundClasses = []

        for cls in self.classes:
            # Only process sub-classes of given super-class
            if not isinstance(cls, (type, types.ClassType)) \
            or not issubclass(cls, self.superClass):
                continue

            # Query class whether it feels suitable
            testMeth = getattr(cls, self.testMethName)
            if testMeth and testMeth(search):
                foundClasses.append(cls)

        # Return if suitable classes has been found.
        if foundClasses:
            return foundClasses

        # No class found. Raise exception
        raise appexceptions.NoClassFound()


    def lookup(self, search):
        '''
        The lookup method as used by clients. Firs tries to satisfy the search
        from the cache. In case of a miss a deep scan of the provided package
        is conducted. Returns the found class object if successfull. Raises
        appexceptions.NoClassFound otherwise.
        '''
        # Lookup cache
        try:
            return self.lookupCache(search)
        except appexceptions.NoClassFound:
            pass

        # Perform deep scan and remember result
        try:
            foundClasses = self.scanClasses(search)
            self.appendCache(search, foundClasses)

            return foundClasses
        except appexceptions.NoClassFound:
            raise appexceptions.NoClassFound()
