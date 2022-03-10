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

from tkinter import *

from tasks.task_ui.axis_key_controller import *

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

__class_name__ = "TaskGUI"
"""Task name."""

#endregion

class GUI():

#region Attributes

    __logger = None

    __master = None

    __Lab = None

    __controller = None

    __speed = 100

    __key_controllers = []

    __speeds = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    __positions = []

#endregion

#region Constructor

    def __init__(self, **kwargs):

        # if "logger" in kwargs:
        #     self.__logger = kwargs["logger"]

        if "controller" in kwargs:
            self.__controller = kwargs["controller"]

#endregion

#region Private Methods (Robot)

    def __update_robot(self):

        self.__controller.move_speed(self.__speeds)

        moving_bits = self.__controller.is_moving()
        self.__logger.debug("Bits: {}".format(moving_bits))

#endregion

#region Private Methods (Axices CB)

    def __axis_0(self, direction, speed):

        if direction == 0:
            self.__speeds[1] = 0

        elif direction == 1:
            self.__speeds[1] = -speed

        elif direction == -1:
            self.__speeds[1] = speed

        self.__update_robot()

    def __axis_1(self, direction, speed):

        if direction == 0:
            self.__speeds[3] = 0

        elif direction == 1:
            self.__speeds[3] = -speed

        elif direction == -1:
            self.__speeds[3] = speed

        self.__update_robot()

    def __axis_2(self, direction, speed):

        if direction == 0:
            self.__speeds[5] = 0
            self.__speeds[11] = 0

        elif direction == 1:
            self.__speeds[5] = speed
            self.__speeds[11] = -speed

        elif direction == -1:
            self.__speeds[5] = -speed
            self.__speeds[11] = speed

        self.__update_robot()

    def __axis_3(self, direction, speed):

        if direction == 0:
            self.__speeds[7] = 0
            self.__speeds[9] = 0

        elif direction == 1:
            self.__speeds[7] = -speed
            self.__speeds[9] = speed

        elif direction == -1:
            self.__speeds[7] = speed
            self.__speeds[9] = -speed

        self.__update_robot()

    def __axis_4(self, direction, speed):

        if direction == 0:
            self.__speeds[7] = 0
            self.__speeds[9] = 0

        elif direction == 1:
            self.__speeds[7] = speed
            self.__speeds[9] = speed

        elif direction == -1:
            self.__speeds[7] = -speed
            self.__speeds[9] = -speed

        self.__update_robot()

    def __axis_5(self, direction, speed):

        if direction == 0:
            self.__speeds[11] = 0

        elif direction == 1:
            self.__speeds[11] = speed

        elif direction == -1:
            self.__speeds[11] = -speed

        self.__update_robot()

#endregion

#region Private Methods (Keys CB)

    def __key_up(self, event):
        message = 'up {}'.format(event.char)
        self.__Lab.config(text=message)

    def __key_down(self, event):
        message = 'down {}'.format(event.char)
        self.__Lab.config(text=message)

        for key_controller in self.__key_controllers:
            if event.char == key_controller.key_cw:
                key_controller.set_cw()

            elif event.char == key_controller.key_ccw:
                key_controller.set_ccw()

        if event.char == " ":
            for key_controller in self.__key_controllers:
                key_controller.stop()


        elif event.char == "p":
            position = self.__controller.current_position()
            msg = "Current position: {}".format(position)
            print(msg)
        
        elif event.char == "s":
            position = self.__controller.current_position()
            self.__positions.append(position)
            msg = "Stored position: {}".format(position)
            print(msg)

        elif event.char == "l":
            for position in self.__positions:
                msg = "Stored position: {}".format(position)
                print(msg)

        elif event.char == "g":
            for position in self.__positions:
                self.__controller.move_relative(position)
                c_position = self.__controller.current_position()
                msg = "Current position: {}".format(c_position)
                print(msg)

#endregion

#region Private Methods (UI)

    def __create_form(self):

        self.__master = Tk()
        self.__master.geometry("300x300")
        self.__master.title("Robko 01")

        # Bind keys.
        self.__master.bind_all("<KeyPress>", self.__key_down)
        self.__master.bind_all("<KeyRelease>", self.__key_up)

        display='Press Any Button, or Press  Key'
        self.__Lab = Label(self.__master, text=display, width=len(display))
        self.__Lab.pack(pady=40)
        # self.__Lab.bind_all('<Key>', self.key)

        self.__master.mainloop()

#endregion

#region Public Methods

    def start(self):

        if self.__logger is None:
            self.__logger = get_logger(__name__)

        # Key controllers.
        self.__key_controllers.append(AxisKeyController(key_cw="1", key_ccw="q", callback=self.__axis_0, speed=self.__speed))
        self.__key_controllers.append(AxisKeyController(key_cw="2", key_ccw="w", callback=self.__axis_1, speed=self.__speed))
        self.__key_controllers.append(AxisKeyController(key_cw="3", key_ccw="e", callback=self.__axis_2, speed=self.__speed))
        self.__key_controllers.append(AxisKeyController(key_cw="4", key_ccw="r", callback=self.__axis_3, speed=self.__speed))
        self.__key_controllers.append(AxisKeyController(key_cw="5", key_ccw="t", callback=self.__axis_4, speed=self.__speed))
        self.__key_controllers.append(AxisKeyController(key_cw="6", key_ccw="y", callback=self.__axis_5, speed=self.__speed))

        # The UI.
        self.__create_form()

#endregion
