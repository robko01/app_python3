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
from struct import pack, unpack

from App.controllers.orlin369.protocol.package_manager import PackageManager

from controllers.base_robko01 import BaseRobko01
from controllers.orlin369.op_code import OpCode
from controllers.orlin369.status_code import StatusCode

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

class Robko01(BaseRobko01):
    """This class is dedicated to controll robot controller made by Orlin Dimitrov."""

    __comunicator = None

    __pm = None

#region Constructor

    def __init__(self, communicator):

        if communicator is None:
            raise ValueError("Communicator can not be None.")

        self.__communicator = communicator

        self.__pm = PackageManager(self.__communicator)

#endregion

#region Public Methods

    def connect(self):
        """Connect to the robot controller."""

        self.__communicator.connect()

    def disconnect(self):
        """Disconnect from robot controller."""

        self.__communicator.disconnect()

    def wait_for_controller(self):
        """WAit for robot controller to become active."""

        response = None

        self.__communicator.reset()

        payload = [48, 48, 48, 48, 48, 48, 48, 48]
        times = 0
        while True:
            response = self.ping(payload)
            if response.is_valid():
                if response.payload_is(payload):
                    break

            times += 1
            if times > self._timeout:
                raise TimeoutError("Controller does not respond.")

            time.sleep(self._sync_interval)

        return response

    def wait_to_stop(self):
        """Wait robot to stop moving."""

        response = self.is_moving()

        while response != 0:
            response = self.is_moving()

            time.sleep(self._sync_interval)


    def ping(self, payload):
        """Ping the robot controller.

        Parameters
        ----------
        payload : array
            Ping payload.

        Returns
        -------
        array
            Answer payload.
        """

        if payload is None:
            raise ValueError("Payload can not be None")

        response = None

        while True:
            response = self.__pm.request(OpCode.Ping.value, payload)
            if response.is_valid():
                if response.status == StatusCode.Ok.value:
                    if response.opcode == OpCode.Ping.value:
                        break
                    else:
                        print("Ping: Invalid operation code: " + str(ord(response.opcode)))
                else:
                    print("Status: " + StatusCode.to_text(response.status) \
                      + "; OpCode: " + OpCode.to_text(response.opcode))
            else:
                print("Ping: Invalid package.")

            time.sleep(self._sync_interval)

        return response

    def stop(self):
        """Stop robot motion execution.

        Returns
        -------
        mixed
            Communicator response.
        """

        response = None

        while True:
            response = self.__pm.request(OpCode.Stop.value)
            if response.is_valid():
                if response.status == StatusCode.Ok.value:
                    if response.opcode == OpCode.Stop.value:
                        break
                    else:
                        print("Stop: Invalid operation code: " + str(response.opcode))
                else:
                    print("Status: " + StatusCode.to_text(response.status) \
                      + "; OpCode: " + OpCode.to_text(response.opcode))
            else:
                print("Stop: Invalid package.")

            time.sleep(self._sync_interval)

        return response

    def disable(self):
        """Stop robot motion execution.

        Returns
        -------
        mixed
            Communicator response.
        """

        response = None

        while True:
            response = self.__pm.request(OpCode.Disable.value)
            if response.is_valid():
                if response.status == StatusCode.Ok.value:
                    if response.opcode == OpCode.Disable.value:
                        break
                    else:
                        print("Disable: Invalid operation code: " + str(response.opcode))
                else:
                    print("Status: " + StatusCode.to_text(response.status) \
                      + "; OpCode: " + OpCode.to_text(response.opcode))
            else:
                print("Disable: Invalid package.")

            time.sleep(self._sync_interval)

        return response

    def enable(self):
        """Enable robot motion execution.

        Returns
        -------
        mixed
            Communicator response.
        """

        response = None

        while True:
            response = self.__pm.request(OpCode.Enable.value)
            if response.is_valid():
                if response.status == StatusCode.Ok.value:
                    if response.opcode == OpCode.Enable.value:
                        break
                    else:
                        print("Enable: Invalid operation code: " + str(response.opcode))
                else:
                    print("Status: " + StatusCode.to_text(response.status) \
                      + "; OpCode: " + OpCode.to_text(response.opcode))
            else:
                print("Enable: Invalid package.")

            time.sleep(self._sync_interval)

        return response

    def clear(self):
        """Clear robot position.

        Returns
        -------
        mixed
            Communicator response.
        """

        response = None

        while True:
            response = self.__pm.request(OpCode.Clear.value)
            if response.is_valid():
                if response.status == StatusCode.Ok.value:
                    if response.opcode == OpCode.Clear.value:
                        break
                    else:
                        print("Clear: Invalid operation code: " + str(response.opcode))
                else:
                    print("Status: " + StatusCode.to_text(response.status) \
                      + "; OpCode: " + OpCode.to_text(response.opcode))
            else:
                print("Clear: Invalid package.")

            time.sleep(self._sync_interval)

        return response

    def move_relative(self, current_point):
        """Move relative to next robot position.

        Parameters
        ----------
        current_point : array
            New robot position.

        Returns
        -------
        mixed
            Communicator response.
        """

        response = None

        while True:

            payload = pack("<hhhhhhhhhhhh",\
                int(current_point[0]), int(current_point[1]),\
                int(current_point[2]), int(current_point[3]),\
                int(current_point[4]), int(current_point[5]),\
                int(current_point[6]), int(current_point[7]),\
                int(current_point[8]), int(current_point[9]),\
                int(current_point[10]), int(current_point[11]))

            response = self.__pm.request(OpCode.MoveRelative.value, payload)

            if response.is_valid():
                if response.status == StatusCode.Ok.value:
                    if response.opcode == OpCode.MoveRelative.value:
                        break
                    else:
                        print("Move Relative: Invalid operation code: " +\
                            str(response.opcode))
                elif response.status == StatusCode.Busy.value:
                    break
                else:
                    print("Status: " + StatusCode.to_text(response.status) \
                      + "; OpCode: " + OpCode.to_text(response.opcode))
            else:
                print("Move Relative: Invalid package.")

        if self.synchronous:
            self.wait_to_stop()

        return response

    def move_absolute(self, current_point):
        """Move absolute to next robot position.

        Parameters
        ----------
        current_point : array
            New robot position.

        Returns
        -------
        mixed
            Communicator response.
        """

        response = None

        while True:

            payload = pack("<hhhhhhhhhhhh",\
                int(current_point[0]), int(current_point[1]),\
                int(current_point[2]), int(current_point[3]),\
                int(current_point[4]), int(current_point[5]),\
                int(current_point[6]), int(current_point[7]),\
                int(current_point[8]), int(current_point[9]),\
                int(current_point[10]), int(current_point[11]))

            response = self.__pm.request(OpCode.MoveAbsolute.value, payload)

            if response.is_valid():
                if response.status == StatusCode.Ok.value:
                    if response.opcode == OpCode.MoveAbsolute.value:
                        break
                    else:
                        print("Move Absolute: Invalid operation code: " +\
                            str(response.opcode))
                elif response.status == StatusCode.Busy.value:
                    break
                else:
                    print("Status: " + StatusCode.to_text(response.status) \
                      + "; OpCode: " + OpCode.to_text(response.opcode))
            else:
                print("Move Absolute: Invalid package.")

            time.sleep(self._sync_interval)

        if self.synchronous:
            self.wait_to_stop()

        return response

    def is_moving(self):
        """Is robot si moving.

        Returns
        -------
        int
            Bit masking of robot motion.
        """

        response = None
        result = 0

        while True:

            response = self.__pm.request(OpCode.IsMoving.value)

            if response.is_valid():
                if response.status == StatusCode.Ok.value:
                    if response.opcode == OpCode.IsMoving.value:
                        value = response.payload
                        result = value[0]
                        #print("Is Moving: " + str(self.__int_to_bin(bytes(value))))
                        break
                    else:
                        print("Invalid operation code: " + str(response.opcode))
                else:
                    print("Status: " + StatusCode.to_text(response.status) \
                      + "; OpCode: " + OpCode.to_text(response.opcode))
            else:
                print("Is Moving: Invalid package.")

            time.sleep(self._sync_interval)

        return result

    def current_position(self):
        """Current robot position.

        Returns
        -------
        array
            Robot positions.
        """

        response = None
        position = None

        while True:
            response = self.__pm.request(OpCode.CurrentPosition.value)
            if response.is_valid():
                if response.status == StatusCode.Ok.value:
                    if response.opcode == OpCode.CurrentPosition.value:
                        value = response.payload
                        position = unpack("<hhhhhhhhhhhh", bytes(value))
                        break
                    else:
                        print("Current Position: Invalid operation code: " +\
                            str(response.opcode))
                else:
                    print("Status: " + StatusCode.to_text(response.status) \
                      + "; OpCode: " + OpCode.to_text(response.opcode))
            else:
                print("Current Position: Invalid package.")

            time.sleep(self._sync_interval)

        return position

    def get_inputs(self):
        """Current robot inputs.

        Returns
        -------
        array
            Inputs of the robot.
        """

        response = None
        output = None

        while True:

            response = self.__pm.request(OpCode.DI.value)

            if response.is_valid():
                if response.status == StatusCode.Ok.value:
                    if response.opcode == OpCode.DI.value:
                        value = response.payload
                        #print("Inputs: " + str(self.__int_to_bin(bytes(value))))
                        output = value
                        break
                    else:
                        print("Digital Inputs: Invalid operation code: " + \
                            str(response.opcode))
                else:
                    print("Status: " + StatusCode.to_text(response.status) \
                      + "; OpCode: " + OpCode.to_text(response.opcode))
            else:
                print("Digital Inputs: Invalid package.")

            time.sleep(self._sync_interval)

        return response, output

    def set_outputs(self, value):
        """Set robot outputs.

        Parameters
        ----------
        value : int
            New robot position.

        Returns
        -------
        mixed
            Communicator response.
        """

        response = None

        while True:
            response = self.__pm.request(OpCode.DO.value)

            if response.is_valid():
                if response.status == StatusCode.Ok.value:
                    if response.opcode == OpCode.DO.value:
                        arr = [int(x) for x in bin(value)[2:]]
                        print("Digital Outputs: " + str(arr))
                        break
                    else:
                        print("Digital Outputs: Invalid operation code: " + \
                            str(response.opcode))
                else:
                    print("Status: " + StatusCode.to_text(response.status) \
                      + "; OpCode: " + OpCode.to_text(response.opcode))
            else:
                print("Digital Outputs: Invalid package.")

            time.sleep(self._sync_interval)

        return response

    def move_speed(self, current_point):
        """Move the robot in speed mode.

        Parameters
        ----------
        current_point : array
            New robot direction.

        Returns
        -------
        mixed
            Communicator response.
        """

        response = None

        while True:

            payload = pack("<hhhhhhhhhhhh",\
                current_point[0], current_point[1],\
                current_point[2], current_point[3],\
                current_point[4], current_point[5],\
                current_point[6], current_point[7],\
                current_point[8], current_point[9],\
                current_point[10], current_point[11])

            response = self.__pm.request(OpCode.MoveSpeed.value, payload)
            if response.is_valid():
                if response.status == StatusCode.Ok.value:
                    if response.opcode == OpCode.MoveSpeed.value:
                        break
                    else:
                        print("Move Speed: Invalid operation code: " + str(response.opcode))
                elif response.status == StatusCode.Busy.value:
                    break
                else:
                    print("Status: " + StatusCode.to_text(response.status) \
                      + "; OpCode: " + OpCode.to_text(response.opcode))
            else:
                print("Move Speed: Invalid package.")

            time.sleep(self._sync_interval)

        if self.synchronous:
            self.wait_to_stop()

        return response


    def move_relative_base(self, steps, speed):
        """Move axis in relative mode.

        Parameters
        ----------
        steps : int
            Axis steps.
        speed : int
            Axis speed.

        Returns
        -------
        mixed
            Communicator response.
        """

        point = [steps, speed, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        return self.move_relative(point)

    def move_relative_shoulder(self, steps, speed):
        """Move axis in relative mode.

        Parameters
        ----------
        steps : int
            Axis steps.
        speed : int
            Axis speed.

        Returns
        -------
        mixed
            Communicator response.
        """

        point = [0, 0, steps, speed, 0, 0, 0, 0, 0, 0, 0, 0]
        return self.move_relative(point)

    def move_relative_elbow(self, steps, speed):
        """Move axis in relative mode.

        Parameters
        ----------
        steps : int
            Axis steps.
        speed : int
            Axis speed.

        Returns
        -------
        mixed
            Communicator response.
        """

        point = [0, 0, 0, 0, steps, speed, 0, 0, 0, 0, -steps, speed]
        return self.move_relative(point)

    def move_relative_r(self, steps, speed):
        """Move axis in relative mode.

        Parameters
        ----------
        steps : int
            Axis steps.
        speed : int
            Axis speed.

        Returns
        -------
        mixed
            Communicator response.
        """

        point = [0, 0, 0, 0, 0, 0, steps, speed, steps, speed, 0, 0]
        return self.move_relative(point)

    def move_relative_p(self, steps, speed):
        """Move axis in relative mode.

        Parameters
        ----------
        steps : int
            Axis steps.
        speed : int
            Axis speed.

        Returns
        -------
        mixed
            Communicator response.
        """

        point = [0, 0, 0, 0, 0, 0, steps, speed, -steps, speed, 0, 0]
        return self.move_relative(point)

    def move_relative_gripper(self, steps, speed):
        """Move axis in relative mode.

        Parameters
        ----------
        steps : int
            Axis steps.
        speed : int
            Axis speed.

        Returns
        -------
        mixed
            Communicator response.
        """

        point = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, steps, speed]
        return self.move_relative(point)


    def move_absolute_base(self, steps, speed):
        """Move axis in absolute mode.

        Parameters
        ----------
        steps : int
            Axis steps.
        speed : int
            Axis speed.

        Returns
        -------
        mixed
            Communicator response.
        """

        point = [steps, speed, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        return self.move_absolute(point)

    def move_absolute_shoulder(self, steps, speed):
        """Move axis in absolute mode.

        Parameters
        ----------
        steps : int
            Axis steps.
        speed : int
            Axis speed.

        Returns
        -------
        mixed
            Communicator response.
        """

        point = [0, 0, steps, speed, 0, 0, 0, 0, 0, 0, 0, 0]
        return self.move_absolute(point)

    def move_absolute_elbow(self, steps, speed):
        """Move axis in absolute mode.

        Parameters
        ----------
        steps : int
            Axis steps.
        speed : int
            Axis speed.

        Returns
        -------
        mixed
            Communicator response.
        """

        point = [0, 0, 0, 0, steps, speed, 0, 0, 0, 0, -steps, speed]
        return self.move_absolute(point)

    def move_absolute_r(self, steps, speed):
        """Move axis in absolute mode.

        Parameters
        ----------
        steps : int
            Axis steps.
        speed : int
            Axis speed.

        Returns
        -------
        mixed
            Communicator response.
        """

        point = [0, 0, 0, 0, 0, 0, steps, speed, steps, speed, 0, 0]
        return self.move_absolute(point)

    def move_absolute_p(self, steps, speed):
        """Move axis in absolute mode.

        Parameters
        ----------
        steps : int
            Axis steps.
        speed : int
            Axis speed.

        Returns
        -------
        mixed
            Communicator response.
        """

        point = [0, 0, 0, 0, 0, 0, steps, speed, -steps, speed, 0, 0]
        return self.move_absolute(point)

    def move_absolute_gripper(self, steps, speed):
        """Move axis in absolute mode.

        Parameters
        ----------
        steps : int
            Axis steps.
        speed : int
            Axis speed.

        Returns
        -------
        mixed
            Communicator response.
        """

        point = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, steps, speed]
        return self.move_absolute(point)

#endregion
