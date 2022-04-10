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

import pygame

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

__status__ = "Debug"
"""File status."""

#endregion

class JoystickController(object):
    """Class representing the PS4 controller. Pretty straightforward functionality.
    """

#region Attributes

    __joystick = None
    """Joystick instance.
    """

    __axis_data = None
    """Axis data.
    """

    __button_data = None
    """Buttons data.
    """

    __hat_data = None
    """Hat data.
    """

    __update_cb = None
    """Update callback.
    """    

#endregion

#region Constructor

    def __init__(self, index=0):
        """Initialize the joystick components.

        Args:
            index (int, optional): Joystick index. Defaults to 0.
        """

        pygame.init()
        pygame.joystick.init()
        self.__joystick = pygame.joystick.Joystick(index)
        self.__joystick.init()

        if not self.__axis_data:
            self.__axis_data = {}

        if not self.__button_data:
            self.__button_data = {}
            for i in range(self.__joystick.get_numbuttons()):
                self.__button_data[i] = False

        if not self.__hat_data:
            self.__hat_data = {}
            for i in range(self.__joystick.get_numhats()):
                self.__hat_data[i] = (0, 0)

#endregion

#region Public Methods

    def update_cb(self, cb):

        if cb != None:
            self.__update_cb = cb

    def update(self):
        """Listen for events to happen.
        """

        events = pygame.event.get()

        for event in events:

            if event.type == pygame.JOYAXISMOTION:
                self.__axis_data[event.axis] = round(event.value, 2)

            elif event.type == pygame.JOYBUTTONDOWN:
                self.__button_data[event.button] = True

            elif event.type == pygame.JOYBUTTONUP:
                self.__button_data[event.button] = False

            elif event.type == pygame.JOYHATMOTION:
                self.__hat_data[event.hat] = event.value

        if self.__update_cb != None:
            self.__update_cb(self.__button_data, self.__axis_data, self.__hat_data)

#endregion
