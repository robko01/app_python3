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

from enum import Enum

from utils.utils import scale_speeds
from utils.logger import get_logger

from kbd import KBD

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

class ExecutionMode(Enum):
    """Execution mode."""

    Pause = 0
    """Pause the execution."""

    Step = 1
    """Step by step mode."""

    Continue = 2
    """Continue execution mode."""

class RobotTaskManager:
    """This class handles the robot tasks in nice procedure way."""

#region Attributes

    __logger = None
    """Logger"""

    __controller = None
    """Robot controller."""

    __execution_mode = ExecutionMode.Pause
    """Mode of execution."""

    __program_name = ""
    """Program name."""

    __key_bd = None

#endregion

#region Properties

    @property
    def execution_mode(self):
        """Execution mode.

        Returns
        -------
        ExecutionMode
            Execution mode.
        """

        return self.__execution_mode

    @execution_mode.setter
    def execution_mode(self, mode):
        """Set execution mode.

        Parameters
        ----------
        mode : ExecutionMode
            Execution mode.
        """

        self.__execution_mode = mode

#endregion

#region Constructor

    def __init__(self, controller):
        """Constructor

        Parameters
        ----------
        controller : mixed
            Robot controller.
        """
        self.__logger = get_logger(__name__)
        self.__controller = controller

#endregion

    def stop(self):
        """Stop robot controller."""

        # Stop all the motors.
        self.__controller.stop()

        # Disable motors.
        self.__controller.disable()

        if self.__program_name == "kb":
            if self.__key_bd is not None:
                self.__key_bd.stop()

    def start(self):
        """Start robot controller."""

        # Enter synchronous mode.
        self.__controller.synchronous = True

        # Wait for controller to respond.
        self.__controller.wait_for_controller()

        # Enable the motors.
        self.__controller.enable()

    def run(self, program=None):
        """Set execution mode.

        Parameters
        ----------
        program : str
            Program name.
        """

        self.__program_name = program

        self.__controller.connect()

        if self.__program_name == "manual":
            self.__prg_manual()

        elif self.__program_name == "grasp1":
            self.__prg_robot_grasp1()

        elif self.__program_name == "grasp2":
            self.__prg_robot_grasp2()

        elif self.__program_name == "grasp3":
            self.__prg_robot_grasp3()

        elif self.__program_name == "inputs":
            self.__read_inputs()

        elif self.__program_name == "kb":
            self.__prg_kb()

        elif  self.__program_name is not None:
            self.__logger.error("No program selected")

        else:
            self.__logger.error("No program selected")

        self.__controller.disconnect()

    def __prg_kb(self):

        self.__logger.info("KB")

        if self.__key_bd is None:
            self.__key_bd = KBD(self.__controller)
            self.__key_bd.start()

    def __prg_manual(self):

        # TODO:Add user interface.

        self.start()

        poses = []
        while True:
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

    def __prg_robot_grasp1(self):

        self.start()

        # Set the speed.
        speed = 100

        # Trajectory but like commands.
        self.__controller.move_relative_base(450, speed)
        self.__controller.move_relative_shoulder(600, speed)
        self.__controller.move_relative_p(200, speed)
        self.__controller.move_relative_elbow(-400, speed)
        self.__controller.move_relative_r(110, speed)
        self.__controller.move_relative_shoulder(100, speed)
        self.__controller.move_relative_gripper(-10, speed)
        self.__controller.move_relative_shoulder(-100, speed)
        self.__controller.move_relative_base(-900, speed)
        self.__controller.move_relative_r(-220, speed)
        self.__controller.move_relative_shoulder(100, speed)
        self.__controller.move_relative_shoulder(-100, speed)
        self.__controller.move_relative_r(110, speed)
        self.__controller.move_relative_elbow(400, speed)
        self.__controller.move_relative_p(-200, speed)
        self.__controller.move_relative_shoulder(-600, speed)
        self.__controller.move_relative_base(450, speed)

        self.stop()

    def __prg_robot_grasp2(self):

        self.start()

        # Set the speed.
        speed = 100

        # Trajectory path.
        trajectory = [ \
            [450, 0, 600, 0, -400, 0, 200, 0, -200, 0, 400, 0], \
            [0, 0, 0, 0, 0, 0, 110, 0, 110, 0, 0, 0], \
            [0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -100, 0], \
            [0, 0, -100, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
            [-900, 0, 0, 0, 0, 0, -200, 0, -200, 0, 0, 0], \
            [0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 100, 0], \
            [0, 0, -100, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
            [0, 0, 0, 0, 0, 0, 110, 0, 110, 0, 0, 0], \
            [450, 0, -600, 0, 400, 0, -220, 0, 180, 0, -400, 0] \
            ]

        command = ""
        for position in trajectory:
            if self.execution_mode == ExecutionMode.Step:
                command = input("Press Enter to continue or type command: ")
                print("Command:", command)

            command = command.lower()

            if command == "continue":
                self.execution_mode = ExecutionMode.Continue

            elif command == "home":
                self.__controller.move_absolute([0, 300, 0, 300, 0, 300, 0, 300, 0, 300, 0, 300])
                break

            print("Target:", position)
            current_point = scale_speeds(position, speed)
            print("Result:", current_point)
            self.__controller.move_relative(current_point)
            current_point = self.__controller.current_position()
            print("Reach:", current_point)
            print("")

        self.stop()

    def __prg_robot_grasp3(self):

        self.start()

        # Set the speed.
        speed = 100

        # Trajectory path.
        trajectory = [ \
            [450, 0, 600, 0, -400, 0, 200, 0, -200, 0, 400, 0], \
            [450, 0, 600, 0, -400, 0, 310, 0, -90, 0, 400, 0], \
            [450, 0, 700, 0, -400, 0, 310, 0, -90, 0, 400, 0], \
            [450, 0, 700, 0, -400, 0, 310, 0, -90, 0, 300, 0], \
            [450, 0, 600, 0, -400, 0, 310, 0, -90, 0, 300, 0], \
            [-450, 0, 600, 0, -400, 0, 110, 0, -290, 0, 300, 0], \
            [-450, 0, 700, 0, -400, 0, 110, 0, -290, 0, 300, 0], \
            [-450, 0, 700, 0, -400, 0, 110, 0, -290, 0, 400, 0], \
            [-450, 0, 600, 0, -400, 0, 110, 0, -290, 0, 400, 0], \
            #[-450, 0, 600, 0, -400, 0, 220, 0, -180, 0, 400, 0], \
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] \
            ]

        for position in trajectory:
            print("Target:", position)
            current_point = scale_speeds(position, speed)
            print("Result:", current_point)
            self.__controller.move_absolute(current_point)
            current_point = self.__controller.current_position()
            print("Reach:", current_point)
            print("")

        self.stop()

    def __read_inputs(self):

        self.start()

        # Read inputs
        inputs = self.__controller.get_inputs()[1]

        # Show it.
        self.__logger.info("Digital Inputs: " + str(inputs))

        self.stop()
