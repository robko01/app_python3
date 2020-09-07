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

from tasks.base_task import BaseTask

from utils.logger import get_logger
from utils.utils import scale_speeds

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

class TaskCmd(BaseTask):
    """Command line test tool."""

#region Public Methods

    def start(self):
        """Start the task."""

        self._start_cont()

        poses = []

        while not self._stop_flag:

            print("")
            command = input("Enter command: ")
            command = command.lower()

            if command == "exit":
                self.stop()
                break

            elif command == "base" or command == "0":
                steps = input("Enter steps: ")
                speed = input("Enter speed: ")

                if steps == "":
                    steps = "10"

                if speed == "":
                    speed = "10"

                steps = int(steps.lower())
                speed = int(speed.lower())

                print("Execute %s @ %d steps and %d speed." % (command, steps, speed))

                self.__controller.move_relative_base(steps, speed)

            elif command == "shoulder" or command == "1":
                steps = input("Enter steps: ")
                speed = input("Enter speed: ")

                if steps == "":
                    steps = "10"

                if speed == "":
                    speed = "10"

                steps = int(steps.lower())
                speed = int(speed.lower())

                print("Execute %s @ %d steps and %d speed." % (command, steps, speed))

                self.__controller.move_relative_shoulder(steps, speed)

            elif command == "elbow" or command == "2":
                steps = input("Enter steps: ")
                speed = input("Enter speed: ")

                if steps == "":
                    steps = "10"

                if speed == "":
                    speed = "10"

                steps = int(steps.lower())
                speed = int(speed.lower())

                print("Execute %s @ %d steps and %d speed." % (command, steps, speed))

                self.__controller.move_relative_elbow(steps, speed)

            elif command == "p" or command == "3":
                steps = input("Enter steps: ")
                speed = input("Enter speed: ")

                if steps == "":
                    steps = "10"

                if speed == "":
                    speed = "10"

                steps = int(steps.lower())
                speed = int(speed.lower())


                print("Execute %s @ %d steps and %d speed." % (command, steps, speed))

                self.__controller.move_relative_p(steps, speed)

            elif command == "r" or command == "4":
                steps = input("Enter steps: ")
                speed = input("Enter speed: ")

                if steps == "":
                    steps = "10"

                if speed == "":
                    speed = "10"

                steps = int(steps.lower())
                speed = int(speed.lower())

                print("Execute %s @ %d steps and %d speed." % (command, steps, speed))

                self.__controller.move_relative_r(steps, speed)

            elif command == "gripper" or command == "5":
                steps = input("Enter steps: ")
                speed = input("Enter speed: ")

                if steps == "":
                    steps = "10"

                if speed == "":
                    speed = "10"

                steps = int(steps.lower())
                speed = int(speed.lower())

                print("Execute %s @ %d steps and %d speed." % (command, steps, speed))

                self.__controller.move_relative_gripper(steps, speed)

            elif command == "pos":

                current_point = self.__controller.current_position()
                print("Current position:", current_point)

            elif command == "add_c_pos":

                current_point = self.__controller.current_position()
                print("Current position:", current_point)
                poses.append(current_point)

            elif command == "ls_pos":

                print("Current positions:")
                print(poses)

            else:
                print("Invalid command: {}".format(command))

#endregion
