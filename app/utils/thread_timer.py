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

import threading
import time

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

__class_name__ = "TaskGUI"
"""Task name."""

#endregion

class ThreadTimer():

#region Attributes

    __exit_event = None
    """Exit event.
    """    

    __thread = None
    """GUI thread.
    """

    __update_rate = 0.1
    """Update rate in seconds.
    """

#endregion

#region Properties

    @property
    def update_rate(self):

        return self.__update_rate

    @update_rate.setter
    def update_rate(self, value):

        self.__update_rate = value

#endregion

#region Constructor

    def __init__(self):

        pass

#endregion

#region Private Methods

    def __thread_worker(self):

        t0 = 0
        t1 = 0
        delta_t = 0

        while True:

            t1 = time.time()
            delta_t = t1 - t0
            if delta_t >= self.__update_rate:
                t0 = t1
    
                if self.__cb != None:
                    self.__cb()

            if self.__exit_event.is_set():
                break

        if self.__exit_event != None:
            del self.__exit_event

        if self.__thread != None:
            del self.__thread

#endregion

#region Public Methods

    def start(self):

        self.__exit_event = threading.Event()

        self.__thread = threading.Thread(target=self.__thread_worker)

        if self.__thread != None:
            self.__thread.daemon = True
            self.__thread.start()

    def stop(self):

        if self.__exit_event != None:
            self.__exit_event.set()

        if self.__thread != None:
            self.__thread.join()

    def set_cb(self, cb):

        if cb != None:
            self.__cb = cb

#endregion
