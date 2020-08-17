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

from enum import Enum

from utils.utils import scale_speeds
from utils.logger import get_logger

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

    def start(self):
        """Start robot controller."""

        # Enter synchronious mode.
        self.__controller.synchronious = True

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

        self.__controller.connect()

        if program == "manual":
            self.__prg_manual()

        elif program == "grasp1":
            self.__prg_robot_grasp1()

        elif program == "grasp2":
            self.__prg_robot_grasp2()

        elif program == "grasp3":
            self.__prg_robot_grasp3()

        elif program == "inputs":
            self.__read_inputs()

        elif program == "kb":
            self.__prg_kb()

        elif program == "load":
            self.__load()

        elif  program is not None:
            self.__logger.error("No program selcted")

        else:
            self.__logger.error("No program selcted")

        self.__controller.disconnect()

    def __prg_kb(self):
        self.__logger.info("KB")

        speed = 100

        # Start the robot controller.
        self.start()

        # Show position.
        current_point = self.__controller.current_position()
        self.__logger.info("Position:", current_point)

        # It si now ready.
        self.__logger.info("-=<Ready>=-")

        # Get to top of the workpeace.
        target_position = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        # Use keyboard input.
        from inputs import get_key

        # Time to stop flag.
        time_to_stop = False
        action_flag = False

        # Wait user input.
        while not self.__controller.time_to_stop:

            # Get keys.
            events = get_key()

            # Parse events.
            for event in events:

                # Print events.
                self.__logger.info(event.ev_type, event.code, event.state)

                # Time to stop event.
                if ((event.ev_type == 'Key') and \
                    (event.code == 'KEY_ESC') and \
                    (event.state == 1)):
                    time_to_stop = True
                    action_flag = False

                # Q - Read current position.
                if ((event.ev_type == 'Key') and \
                    (event.code == 'KEY_Q') and \
                    (event.state == 1)):
                    # Show position.
                    current_point = self.__controller.current_position()
                    self.__logger.info("Position:", current_point)

                # W - Up wrist
                if ((event.ev_type == 'Key') and \
                    (event.code == 'KEY_W') and \
                    (event.state == 1)):
                    self.__logger.info("Start wrist up.")
                    target_position[7] = speed
                    target_position[9] = -speed
                    action_flag = True
                elif ((event.ev_type == 'Key') and \
                    (event.code == 'KEY_W') and \
                    (event.state == 0)):
                    self.__logger.info("Stop wrist up.")
                    target_position[7] = 0
                    target_position[9] = 0
                    action_flag = True

                # S - Down wrist
                if ((event.ev_type == 'Key') and \
                    (event.code == 'KEY_S') and \
                    (event.state == 1)):
                    self.__logger.info("Start wrist down")
                    target_position[7] = -speed
                    target_position[9] = speed
                    action_flag = True
                elif ((event.ev_type == 'Key') and \
                    (event.code == 'KEY_S') and \
                    (event.state == 0)):
                    self.__logger.info("Stop wrist down.")
                    target_position[7] = 0
                    target_position[9] = 0
                    action_flag = True

                # A - Left wrist
                if ((event.ev_type == 'Key') and \
                    (event.code == 'KEY_A') and \
                    (event.state == 1)):
                    self.__logger.info("Start Left wrist")
                    target_position[7] = -speed
                    target_position[9] = -speed
                    action_flag = True
                elif ((event.ev_type == 'Key') and \
                    (event.code == 'KEY_A') and \
                    (event.state == 0)):
                    self.__logger.info("Stop Left wrist")
                    target_position[7] = 0
                    target_position[9] = 0
                    action_flag = True

                # D - Right wrist
                if ((event.ev_type == 'Key') and \
                    (event.code == 'KEY_D') and \
                    (event.state == 1)):
                    self.__logger.info("Right wrist")
                    target_position[7] = speed
                    target_position[9] = speed
                    action_flag = True
                elif ((event.ev_type == 'Key') and \
                    (event.code == 'KEY_D') and \
                    (event.state == 0)):
                    self.__logger.info("Stop Left wrist")
                    target_position[7] = 0
                    target_position[9] = 0
                    action_flag = True

                # R - Elbow CCW
                if ((event.ev_type == 'Key') and \
                    (event.code == 'KEY_R') and \
                    (event.state == 1)):
                    self.__logger.info("Start Elbow CCW")
                    target_position[5] = speed
                    target_position[11] = speed
                    action_flag = True
                elif ((event.ev_type == 'Key') and \
                    (event.code == 'KEY_R') and \
                    (event.state == 0)):
                    self.__logger.info("Stop Elbow CCW")
                    target_position[5] = 0
                    target_position[11] = 0
                    action_flag = True

                # F - Elbow CW
                if ((event.ev_type == 'Key') and \
                    (event.code == 'KEY_F') and \
                    (event.state == 1)):
                    self.__logger.info("Start Elbow CW")
                    target_position[5] = -speed
                    target_position[11] = -speed
                    action_flag = True
                elif ((event.ev_type == 'Key') and \
                    (event.code == 'KEY_F') and \
                    (event.state == 0)):
                    self.__logger.info("Stop Elbow CW")
                    target_position[5] = 0
                    target_position[11] = 0
                    action_flag = True

                # Arrow Up - Shoulder CCW
                if ((event.ev_type == 'Key') and \
                    (event.code == 'KEY_UP') and \
                    (event.state == 1)):
                    self.__logger.info("Start Shoulder CCW")
                    target_position[3] = speed
                    action_flag = True
                elif ((event.ev_type == 'Key') and \
                    (event.code == 'KEY_UP') and \
                    (event.state == 0)):
                    self.__logger.info("Stop Shoulder CCW")
                    target_position[3] = 0
                    action_flag = True

                # Arrow Down - Shoulder CW
                if ((event.ev_type == 'Key') and \
                    (event.code == 'KEY_DOWN') and \
                    (event.state == 1)):
                    self.__logger.info("Start Shoulder CW")
                    target_position[3] = -speed
                    action_flag = True
                elif ((event.ev_type == 'Key') and \
                    (event.code == 'KEY_DOWN') and \
                    (event.state == 0)):
                    self.__logger.info("Stop Shoulder CW")
                    target_position[3] = 0
                    action_flag = True

                # Arrow Left - Base CW
                if ((event.ev_type == 'Key') and \
                    (event.code == 'KEY_LEFT') and \
                    (event.state == 1)):
                    self.__logger.info("Start Shoulder CW")
                    target_position[1] = speed
                    action_flag = True
                elif ((event.ev_type == 'Key') and \
                    (event.code == 'KEY_LEFT') and \
                    (event.state == 0)):
                    self.__logger.info("Stop Shoulder CW")
                    target_position[1] = 0
                    action_flag = True

                # Arrow Right - Base CW
                if ((event.ev_type == 'Key') and \
                    (event.code == 'KEY_RIGHT') and \
                    (event.state == 1)):
                    self.__logger.info("Start Base CW")
                    target_position[1] = -speed
                    action_flag = True
                elif ((event.ev_type == 'Key') and \
                    (event.code == 'KEY_RIGHT') and \
                    (event.state == 0)):
                    self.__logger.info("Stop Base CW")
                    target_position[1] = 0
                    action_flag = True

                # Execute key command.
                if action_flag:
                    action_flag = False
                    self.__logger.info("Target speeds:", target_position)
                    self.__controller.move_speed(target_position)
                    current_point = self.__controller.current_position()
                    self.__logger.info("Reach:", current_point)

            if time_to_stop:
                self.stop()
                break

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

                self.__controller.move_realtive_base(steps, speed)

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

                self.__controller.move_realtive_shoulder(steps, speed)

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

                self.__controller.move_realtive_elbow(steps, speed)

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

                self.__controller.move_realtive_p(steps, speed)

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

                self.__controller.move_realtive_r(steps, speed)

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

                self.__controller.move_realtive_gripper(steps, speed)

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
                print("Invalied command: {}".format(command))

    def __prg_robot_grasp1(self):

        self.start()

        # Set the speed.
        speed = 100

        # Trajectory but like commands.
        self.__controller.move_realtive_base(450, speed)
        self.__controller.move_realtive_shoulder(600, speed)
        self.__controller.move_realtive_p(200, speed)
        self.__controller.move_realtive_elbow(-400, speed)
        self.__controller.move_realtive_r(110, speed)
        self.__controller.move_realtive_shoulder(100, speed)
        self.__controller.move_realtive_gripper(-10, speed)
        self.__controller.move_realtive_shoulder(-100, speed)
        self.__controller.move_realtive_base(-900, speed)
        self.__controller.move_realtive_r(-220, speed)
        self.__controller.move_realtive_shoulder(100, speed)
        self.__controller.move_realtive_shoulder(-100, speed)
        self.__controller.move_realtive_r(110, speed)
        self.__controller.move_realtive_elbow(400, speed)
        self.__controller.move_realtive_p(-200, speed)
        self.__controller.move_realtive_shoulder(-600, speed)
        self.__controller.move_realtive_base(450, speed)

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
            self.__controller.move_realtive(current_point)
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

    def __load(self):
        print("Load program")
