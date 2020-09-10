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

# Use keyboard input.
from pynput.keyboard import Key, Listener

from tasks.base_task import BaseTask

from utils.logger import get_logger
from utils.utils import scale_speeds

from data.commands import Commands

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

class TaskKbd(BaseTask):
    """Keyboard robot controller."""

#region Attributes

    __logger = None
    """Logger"""

    _controller = None
    """Robot controller."""

    __listener = None
    """Keyboard listener."""

    __directions = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    """Axises directions."""

    __stop_flag = False
    """Stop flag."""

    __speed = 150
    """Axis speed."""

    __commands = None
    """Commands for the robot."""

#endregion

#region Private Methods

    def __send_command(self):

        if self._controller is not None:

            print(self.__directions)

            response = self._controller.move_speed(self.__directions)
            if response.is_valid():
                print("OK")

    def __clear_directions(self):

        self.__directions[1] = 0
        self.__directions[3] = 0
        self.__directions[5] = 0
        self.__directions[7] = 0
        self.__directions[9] = 0
        self.__directions[11] = 0

    def __add_cur_position(self):

        # Show position.
        current_point = self._controller.current_position()
        self.__logger.info("Position: {}".format(current_point))

        self.__commands.append(current_point)

        # - Store it to the list of commands.

    def __save_program(self):

        print("Save recorded robot positions.")

    def __play_program(self):

        for command in self.__commands:

            response = self._controller.move_absolute(command)
            if response.is_valid():
                print("OK")

    def __display_program(self):

        for command in self.__commands:

            print(command)


    def __on_press(self, key):

        str_key = str(key).replace("\'", "").lower()

        if str_key == "1":

            if self.__directions[1] == 0:
                self.__directions[1] = self.__speed

            if self.__directions[1] == -self.__speed:
                self.__directions[1] = 0

            self.__send_command()

        elif str_key == "q":

            if self.__directions[1] == 0:
                self.__directions[1] = -self.__speed

            if self.__directions[1] == self.__speed:
                self.__directions[1] = 0

            self.__send_command()

        elif str_key == "2":

            if self.__directions[3] == 0:
                self.__directions[3] = self.__speed

            if self.__directions[3] == -self.__speed:
                self.__directions[3] = 0

            self.__send_command()

        elif str_key == "w":

            if self.__directions[3] == 0:
                self.__directions[3] = -self.__speed

            if self.__directions[3] == self.__speed:
                self.__directions[3] = 0

            self.__send_command()

        elif str_key == "3":

            if self.__directions[5] == 0:
                self.__directions[5] = self.__speed

            if self.__directions[5] == -self.__speed:
                self.__directions[5] = 0

            self.__send_command()

        elif str_key == "e":

            if self.__directions[5] == 0:
                self.__directions[5] = -self.__speed

            if self.__directions[5] == self.__speed:
                self.__directions[5] = 0

            self.__send_command()

        elif str_key == "4":

            if self.__directions[7] == 0:
                self.__directions[7] = self.__speed

            if self.__directions[7] == -self.__speed:
                self.__directions[7] = 0

            self.__send_command()

        elif str_key == "r":

            if self.__directions[7] == 0:
                self.__directions[7] = -self.__speed

            if self.__directions[7] == self.__speed:
                self.__directions[7] = 0

            self.__send_command()

        elif str_key == "5":

            if self.__directions[9] == 0:
                self.__directions[9] = self.__speed

            if self.__directions[9] == -self.__speed:
                self.__directions[9] = 0

            self.__send_command()

        elif str_key == "t":

            if self.__directions[9] == 0:
                self.__directions[9] = -self.__speed

            if self.__directions[9] == self.__speed:
                self.__directions[9] = 0

            self.__send_command()

        elif str_key == "6":

            if self.__directions[11] == 0:
                self.__directions[11] = self.__speed

            if self.__directions[11] == -self.__speed:
                self.__directions[11] = 0

            self.__send_command()

        elif str_key == "y":

            if self.__directions[11] == 0:
                self.__directions[11] = -self.__speed

            if self.__directions[11] == self.__speed:
                self.__directions[11] = 0

            self.__send_command()

        # Stop all axises.
        elif str_key == "p":

            self.__clear_directions()
            self.__send_command()

        # Add point to commands.
        elif str_key == "i":

            self.__add_cur_position()

        # Save current positions.
        elif str_key == "s":

            self.__save_program()

        # Play saved commands.
        elif str_key == "o":

            self.__play_program()

        # Display saved commands.
        elif str_key == "d":

            self.__display_program()


        else:

            print("{0} pressed".format(key))

    def __on_release(self, key):
        # print("{0} release".format(key))
        if key == Key.esc:
            print("Stopping the robot.")
            # Stop listener
            return False

#endregion

#region Public Methods

    def start(self):
        """Start the app."""

        if self.__commands is None:
            self.__commands = Commands()

        if self.__logger is None:
            self.__logger = get_logger(__name__)

        self._start_cont()

        # Show position.
        current_point = self._controller.current_position()
        self.__logger.info("Position: {}".format(current_point))

        if self.__listener is None:

            self.__listener = Listener(\
                on_press=self.__on_press,\
                on_release=self.__on_release)

            self.__listener.start()

        while not self._stop_flag:
            pass

    def stop(self):
        """Stop the app."""

        if self.__listener is not None:

            self.__listener.stop()
            del self.__listener
            self.__listener = None

        self._stop_cont()

#endregion
