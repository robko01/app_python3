#!/usr/bin/env python
# -*- coding: utf8 -*-

"""

Robko 01 - Python Controll Software

Copyright (C) [2020] [Orlin Dimitrov]

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

import time
import threading

from tasks.base_task import BaseTask
from tasks.task_ui.ui import GUI

from utils.logger import get_logger

#region File Attributes

__author__ = "Orlin Dimitrov"
"""Author of the file."""

__copyright__ = "Copyright 2020, Orlin Dimitrov"
"""Copyrighter"""

__credits__ = []
"""Credits"""

__license__ = "GPLv3"
"""License
@see http://www.gnu.org/licenses/"""

__version__ = "1.0.0"
"""Version of the file."""

__maintainer__ = "Orlin Dimitrov"
"""Name of the maintainer."""

__email__ = "robko01@8bitclub.com"
"""E-mail of the author."""

__class_name__ = "TaskUI"
"""Task name."""

#endregion

class TaskUI(BaseTask):
    """UI tool."""

#region Attributes

    __logger = None
    """Logger"""

    __exit_event = None
    """Exit event.
    """    

    __thread_gui = None
    """GUI thread.
    """

#endregion

#region Constructor

    def __init__(self, **kwargs):

        super().__init__(kwargs)

        self._name = __class_name__

#endregion

#region Private Methods (Thread)

    def __thread_start(self):

        self.__exit_event = threading.Event()

        self.__thread_gui = threading.Thread(target=self.__thread_worker)

        if self.__thread_gui != None:
            self.__thread_gui.daemon = True
            self.__thread_gui.start()

    def __thread_stop(self):

        if self.__exit_event != None:
            self.__exit_event.set()

        if self.__thread_gui != None:
            self.__thread_gui.join()

    def __thread_shed(self):
        
        pass
        # print("OK")

    def __thread_worker(self):

        t0 = 0
        t1 = 0
        delta_t = 0

        while True:

            t1 = time.time()
            delta_t = t1 - t0
            if delta_t >= 1:
                t0 = t1
                self.__thread_shed()

            if self.__exit_event.is_set():
                break

        if self.__exit_event != None:
            del self.__exit_event

        if self.__thread_gui != None:
            del self.__thread_gui

#endregion

#region Private Methods (GUI)

    def key(self, event):

        if event.char == event.keysym:
            message ='Normal Key %r' % event.char

        elif len(event.char) == 1:
            message ='Punctuation Key %r (%r)' % (event.keysym, event.char)

        else:
            message ='Special Key %r' % event.keysym

        self.__Lab.config(text=message)

    def do_mouse(self, eventname):

        def mouse_binding(event):
            message = 'Mouse event %s' % eventname
            self.__Lab.config(text=message)

        self.__Lab.bind_all('<%s>'%eventname, mouse_binding)

    def quit(self, event):                           
        print("Double Click, so let's stop") 
        import sys; sys.exit() 

#endregion

#region Interface Methods

    def start(self):
        """Start the task."""

        if self.__logger is None:
            self.__logger = get_logger(__name__)

        # self.__thread_start()

        self._start_cont()

        gui = GUI(controller=self._controller, logger=self.__logger)
        gui.start()

    def stop(self):

        self.__thread_stop()

#endregion
