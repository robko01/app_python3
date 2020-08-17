#!/usr/bin/env python
# -*- coding: utf8 -*-

'''

MIT License

Copyright (c) [2019] [Orlin Dimitrov]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

'''

import time
from struct import pack, unpack
# https://docs.python.org/3/library/struct.html


from controllers.base_robko01 import BaseRobko01
from controllers.orlin369.op_code import OpCode
from controllers.orlin369.status_code import StatusCode

class Robko01(BaseRobko01):
    """This class is dedicated to controll robot controler made by Orlin Dimitrov."""

#region Constructor

    def __init__(self, communicator):

        if communicator is None:
            raise ValueError("Communicator can not be None.")

        self.__communicator = communicator

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
            response = self.__communicator.request(OpCode.Ping.value, payload)
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
            response = self.__communicator.request(OpCode.Stop.value)
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
            response = self.__communicator.request(OpCode.Disable.value)
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
            response = self.__communicator.request(OpCode.Enable.value)
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
            response = self.__communicator.request(OpCode.Clear.value)
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

    def move_realtive(self, current_point):
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

            response = self.__communicator.request(OpCode.MoveRelative.value, payload)

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

        if self.synchronious:
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

            response = self.__communicator.request(OpCode.MoveAblolute.value, payload)

            if response.is_valid():
                if response.status == StatusCode.Ok.value:
                    if response.opcode == OpCode.MoveAblolute.value:
                        break
                    else:
                        print("Move Ablolute: Invalid operation code: " +\
                            str(response.opcode))
                elif response.status == StatusCode.Busy.value:
                    break
                else:
                    print("Status: " + StatusCode.to_text(response.status) \
                      + "; OpCode: " + OpCode.to_text(response.opcode))
            else:
                print("Move Ablolute: Invalid package.")

            time.sleep(self._sync_interval)

        if self.synchronious:
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

            response = self.__communicator.request(OpCode.IsMoving.value)

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
            Robot posirions.
        """

        response = None
        position = None

        while True:
            response = self.__communicator.request(OpCode.CurrentPosition.value)
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

            response = self.__communicator.request(OpCode.DI.value)

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
            response = self.__communicator.request(OpCode.DO.value)

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

            response = self.__communicator.request(OpCode.MoveSpeed.value, payload)
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

        if self.synchronious:
            self.wait_to_stop()

        return response


    def move_realtive_base(self, steps, speed):
        """Move axis in realtive mode.

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
        return self.move_realtive(point)

    def move_realtive_shoulder(self, steps, speed):
        """Move axis in realtive mode.

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
        return self.move_realtive(point)

    def move_realtive_elbow(self, steps, speed):
        """Move axis in realtive mode.

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
        return self.move_realtive(point)

    def move_realtive_r(self, steps, speed):
        """Move axis in realtive mode.

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
        return self.move_realtive(point)

    def move_realtive_p(self, steps, speed):
        """Move axis in realtive mode.

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
        return self.move_realtive(point)

    def move_realtive_gripper(self, steps, speed):
        """Move axis in realtive mode.

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
        return self.move_realtive(point)


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
