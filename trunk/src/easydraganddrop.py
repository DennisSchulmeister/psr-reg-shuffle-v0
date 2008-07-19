#encoding=utf-8

# easydraganddrop.py
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

This module provides the EasyDragAndDrop class. It is a high-level wrapper
for gtk.WIdget's drag and drop event handlers. It connects to all relevant
signals and takes care of all book keeping but it uses remote functions for
checking drop targets and for performing the drop action.
'''

# Public export of module content
__all__ = [
    "EasyDragAndDrop"
]


# Import global modules
import gtk


# Class definition
class EasyDragAndDrop:
    '''
    This class provides a high-level wrapper for gtk.Widget's drag and drop
    signals. It connects to all relevant signals and takes care of all book
    keeping but uses remote functions for checking drop targets and for
    performing the drop action.
    '''

    def __init__(self, srcWidget, dstWidget, checkFunc, actionFunc, dataFunc):
        '''
        Constructor. Takes the following arguments:

        ============ ==========================================================
        Argument     Description
        ============ ==========================================================
        srcWidget    Source widget which acts as drag source
        dstWidget    Destination widget which acts as drop target
        checkFunc    Function which must return True in order to allow drop
        actionFunc   Action function only called after successfull drop.
        dataFunc     Accesor function which returns data dragged from source
        ============ ==========================================================
        '''
        # Remember arguments
        self.srcWidget  = srcWidget
        self.dstWidget  = dstWidget
        self.checkFunc  = checkFunc
        self.actionFunc = actionFunc
        self.dataFunc   = dataFunc

        # Additional data
        self.mouseOverTarget = False
        self.dropAllowed     = False

        # Connect to signals
        dstWidget.drag_dest_set(
            flags   = 0,
            targets = [],
            actions = 0
        )

        dstWidget.connect("drag-motion", self.on_dstWidget__drag_motion)
        dstWidget.connect("drag-leave",  self.on_dstWidget__drag_leave)
        dstWidget.connect("drag-drop",   self.on_dstWidget__drag_drop)


    def on_dstWidget__drag_leave(self, widget, context, timestamp, *user):
        '''
        This signal handler responds to the mouse cursor leaving a drop
        target. Doesn't do much. Removes drag'n'drop highlighting and
        remembers that cursor resides outsite of target.
        '''
        # Remove highlighting
        widget.drag_unhighlight()

        # Remember state
        self.mouseOverTarget = False

        # ATTENTION: Don't set self.dropAllowed = False here. It will break
        # callback of action functions because drag-leave gets emited prior
        # to drag-drop.


    def on_dstWidget__drag_motion(self, widget, context, x, y, timestamp, *user):
        '''
        This signal handler responds to the mouse cursor being over a drop
        target. It notices if the cursor hasn't been over that target before
        and displays drag'n'drop highlighting. Besides that it checks whether
        a drop would be allowed
        '''
        # Disply highlighting if not already done
        if not self.mouseOverTarget:
            widget.drag_highlight()

        # Remember cursor being there
        self.mouseOverTarget = True

        # Check whether drop would be allowed
        if context.get_source_widget() == self.srcWidget:
            self.dropAllowed = self.checkFunc(self.dataFunc())
        else:
            self.dropAllowed = False

        context.drag_status(gtk.gdk.ACTION_COPY, 0L)
        context.drop_reply(True, 0L)

        return True


    def on_dstWidget__drag_drop(self, widget, context, x, y, timestamp, *user):
        '''
        This signal handler responds to an attempted drop action. It checks
        whether the drop action has been approved earlier (during drag-motion
        handler) and calls the dedicated action function if necessary.
        '''
        # Check for approved drop action
        if not self.dropAllowed:
            return False

        # Call action function
        self.actionFunc(
            self.srcWidget,
            self.dstWidget,
            self.dataFunc()
        )

        # Finish drag and drop process
        context.finish(True, 0L)
