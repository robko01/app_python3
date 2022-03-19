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

from dataclasses import field
from email.mime import base
import queue
from tkinter import *

from tasks.task_ui.actions import Actions
from tasks.task_ui.axis_action_controller import *
from tasks.task_ui.led import LedStatus
from tasks.task_ui.led import LedShape
from tasks.task_ui.led import LED

from utils.logger import get_logger
from utils.thread_timer import ThreadTimer
from utils.timer import Timer

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
    """Logger module.
    """

    __master = None
    """Form master object.
    """

    __frm_port_a_input_leds = []
    """Port A input LEDs.
    """

    __frm_axis_labels = []
    """Axis labels.
    """

    __frm_axis_control_leds = []
    """Axis control LEDs.
    """

    __frm_axis_controllers = []
    """Axis controllers.
    """

    __actions_queue = None
    """Actions queue.
    """

    __controller = None
    """Robot controller.
    """

    __speeds = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    """Axis speeds.
    """

    __current_position = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    """Current end-efector position.
    """

    __port_a_inputs = 0
    """Port A inputs.
    """

    __axis_states = 0
    """Axis action states.
    """

    __positions = []
    """Program positions.
    """

#endregion

#region Constructor

    def __init__(self, **kwargs):

        if "controller" in kwargs:
            self.__controller = kwargs["controller"]

        if self.__logger is None:
            self.__logger = get_logger(__name__)

        self.__actions_queue = queue.Queue()

        self.__action_update_timer = ThreadTimer()
        self.__action_update_timer.update_rate = 0.01
        self.__action_update_timer.set_cb(self.__action_timer_cb)

        self.__frm_update_timer = Timer()
        self.__frm_update_timer.update_rate = 0.05
        self.__frm_update_timer.set_cb(self.__frm_update)

        # Key controllers.
        self.__frm_axis_controllers.append(AxisActionController(callback=self.__axis_0))
        self.__frm_axis_controllers.append(AxisActionController(callback=self.__axis_1))
        self.__frm_axis_controllers.append(AxisActionController(callback=self.__axis_2))
        self.__frm_axis_controllers.append(AxisActionController(callback=self.__axis_3))
        self.__frm_axis_controllers.append(AxisActionController(callback=self.__axis_4))
        self.__frm_axis_controllers.append(AxisActionController(callback=self.__axis_5))

#endregion

#region Private Methods (Action Control)

    def __put_action(self, action):

        self.__actions_queue.put(action)

    def __do_action(self, action):

        if action == Actions.NONE:
            pass

        if action == Actions.UpdateSpeeds:
            self.__controller.move_speed(self.__speeds)

        elif action == Actions.UpdateOutputs:
            self.__controller.set_outputs(self.__port_a_outputs)

        elif action == Actions.RunStoredPositions:
            for position in self.__positions:
                self.__controller.move_relative(position)
                c_position = self.__controller.current_position()
                msg = "Current position: {}".format(c_position)
                self.__logger.debug(msg)

    def __action_timer_cb(self):

        self.__axis_states = self.__controller.is_moving()
        self.__port_a_inputs = self.__controller.get_inputs()
        self.__current_position = self.__controller.current_position()

        if not self.__actions_queue.empty():
            action = self.__actions_queue.get()
            self.__do_action(action)

#endregion

#region Private Methods (Axices CB)

    def __axis_0(self, direction, speed):

        if direction == 0:
            self.__speeds[1] = 0

        elif direction == 1:
            self.__speeds[1] = -speed

        elif direction == -1:
            self.__speeds[1] = speed

        self.__put_action(Actions.UpdateSpeeds)

    def __axis_1(self, direction, speed):

        if direction == 0:
            self.__speeds[3] = 0

        elif direction == 1:
            self.__speeds[3] = -speed

        elif direction == -1:
            self.__speeds[3] = speed

        self.__put_action(Actions.UpdateSpeeds)

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

        self.__put_action(Actions.UpdateSpeeds)

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

        self.__put_action(Actions.UpdateSpeeds)

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

        self.__put_action(Actions.UpdateSpeeds)

    def __axis_5(self, direction, speed):

        if direction == 0:
            self.__speeds[11] = 0

        elif direction == 1:
            self.__speeds[11] = speed

        elif direction == -1:
            self.__speeds[11] = -speed

        self.__put_action(Actions.UpdateSpeeds)

#endregion

#region Private Methods (Form)

    def __update_port_a_outputs(self):

        value = 0

        for bit in range(0, 8):
            value += self.__vars[bit].get()

        self.__port_a_outputs = value
        self.__put_action(Actions.UpdateOutputs)

    def __create_port_a_outputs(self):

        self.__vars = []

        # Create the frame.
        self.__lbl_frame = LabelFrame(self.__master, text="DO on port A")

        # Create the check boxes.
        for index in range(0, 8):

            # Bit wight.
            bit_weight = (2**index)

            # Create the check box.
            var = IntVar()
            check = Checkbutton(self.__lbl_frame, variable=var, onvalue=bit_weight, offvalue=0, command=self.__update_port_a_outputs)
            check.grid(row=0, column=index)
            self.__vars.append(var)

        # Place the frame.
        self.__lbl_frame.place(x=33, y=200)


    def __update_port_a_inputs(self):

        if len(self.__frm_port_a_input_leds) == 8:
            led_index = 7
            for index in range(0, 8):
                if (2**index) & self.__port_a_inputs:
                    self.__frm_port_a_input_leds[led_index].turnon()
                else:
                    self.__frm_port_a_input_leds[led_index].turnoff()
                led_index -= 1

    def __create_port_a_inputs(self):

        # Create the frame.
        self.__lbl_frame = LabelFrame(self.__master, text="DI on port A")

        led_w = 20
        led_h = 20

        for index in range(0, 8):

            led = LED(self.__lbl_frame, shape=LedShape.ROUND, status=LedStatus.OFF,
                width=led_w, height=led_h, appearance=RAISED,
                blink=0, bd=1, outline="")
            led.frame.grid(row=0, column=index)

            self.__frm_port_a_input_leds.append(led)

        # Place the frame.
        self.__lbl_frame.place(x=350, y=200)


    def __update_axis_control_leds(self):

        if len(self.__frm_axis_control_leds) == 6:
            for index in range(0, 6):
                if (2**index) & self.__axis_states:
                    self.__frm_axis_control_leds[index].turnon()
                else:
                    self.__frm_axis_control_leds[index].turnoff()

    def __create_axis_control_leds(self):

        # Create the frame.
        self.__lbl_frame = LabelFrame(self.__master, text="Axis control")

        led_w = 20
        led_h = 20

        for index in range(0, 6):

            led = LED(self.__lbl_frame, shape=LedShape.ROUND, status=LedStatus.OFF,
                width=led_w, height=led_h, appearance=RAISED,
                blink=0, bd=1, outline="")
            led.frame.grid(row=0, column=index)

            self.__frm_axis_control_leds.append(led)

        # Place the frame.
        self.__lbl_frame.place(x=350, y=250)


    def __update_axis_label(self):

        for index in range(0, 6):
            text = "P: {}\nV: {}".format(self.__current_position[index*2], self.__current_position[index*2 + 1])
            self.__frm_axis_labels[index].config(text=text)

    def __create_axis_controls(self):

        w_size = 10
        h_size = 10

        # Create the frame.
        self.__frame = Frame(self.__master)

        empty_text = "P: {}\nV: {}".format(0, 0)

        fields = {
            "cw":[
                {
                    "text": "Base CW",
                    "press": lambda event: self.__frm_axis_controllers[0].set_cw(),
                    "release": lambda event: self.__frm_axis_controllers[0].set_ccw()
                },
                {
                    "text": "Shoulder UP",
                    "press": lambda event: self.__frm_axis_controllers[1].set_cw(),
                    "release": lambda event: self.__frm_axis_controllers[1].set_ccw()
                },
                {
                    "text": "Elbow UP",
                    "press": lambda event: self.__frm_axis_controllers[2].set_cw(),
                    "release": lambda event: self.__frm_axis_controllers[2].set_ccw()
                },
                {
                    "text": "P UP",
                    "press": lambda event: self.__frm_axis_controllers[3].set_cw(),
                    "release": lambda event: self.__frm_axis_controllers[3].set_ccw()
                },
                {
                    "text": "R CW",
                    "press": lambda event: self.__frm_axis_controllers[4].set_cw(),
                    "release": lambda event: self.__frm_axis_controllers[4].set_ccw()
                },
                {
                    "text": "Gripper OPEN",
                    "press": lambda event: self.__frm_axis_controllers[5].set_cw(),
                    "release": lambda event: self.__frm_axis_controllers[5].set_ccw()
                },
            ],
            "ccw":[
                {
                    "text": "Base CCW",
                    "press": lambda event: self.__frm_axis_controllers[0].set_ccw(),
                    "release": lambda event: self.__frm_axis_controllers[0].set_cw()
                },
                {
                    "text": "Shoulder DOWN",
                    "press": lambda event: self.__frm_axis_controllers[1].set_ccw(),
                    "release": lambda event: self.__frm_axis_controllers[1].set_cw()
                },
                {
                    "text": "Elbow DOWN",
                    "press": lambda event: self.__frm_axis_controllers[2].set_ccw(),
                    "release": lambda event: self.__frm_axis_controllers[2].set_cw()
                },
                {
                    "text": "P DOWN",
                    "press": lambda event: self.__frm_axis_controllers[3].set_ccw(),
                    "release": lambda event: self.__frm_axis_controllers[3].set_cw()
                },
                {
                    "text": "R CCW",
                    "press": lambda event: self.__frm_axis_controllers[4].set_ccw(),
                    "release": lambda event: self.__frm_axis_controllers[4].set_cw()
                },
                {
                    "text": "Gripper CLOSE",
                    "press": lambda event: self.__frm_axis_controllers[5].set_ccw(),
                    "release": lambda event: self.__frm_axis_controllers[5].set_cw()
                }
            ]
        }

        buttons_cw = []
        buttons_ccw = []

        for index in range(0, 6):

            self.__frm_axis_labels.append(Label(self.__frame, text=empty_text))
            self.__frm_axis_labels[index].grid(row=0, column=index, ipadx=h_size, ipady=w_size, sticky='ew')

            buttons_cw.append(Button(self.__frame, text=fields["cw"][index]["text"]))
            buttons_cw[index].bind("<ButtonPress-1>", fields["cw"][index]["press"])
            buttons_cw[index].bind("<ButtonRelease-1>", fields["cw"][index]["release"])
            buttons_cw[index].grid(row=1, column=index, ipadx=h_size, ipady=w_size, sticky='ew')

            buttons_ccw.append(Button(self.__frame, text=fields["ccw"][index]["text"]))
            buttons_ccw[index].bind("<ButtonPress-1>", fields["ccw"][index]["press"])
            buttons_ccw[index].bind("<ButtonRelease-1>", fields["ccw"][index]["release"])
            buttons_ccw[index].grid(row=2, column=index, ipadx=h_size, ipady=w_size, sticky='ew')

        # Place the frame.
        self.__frame.place(x=33, y=33)


    def __frm_key_release(self, event):
        message = "up {}".format(event.char)
        self.__lbl_buttons_state.config(text=message)

    def __frm_key_press(self, event):

        char = event.char

        message = "down {}".format(char)
        self.__lbl_buttons_state.config(text=message)

        if char == " ":
            for key_controller in self.__frm_axis_controllers:
                key_controller.stop()

        elif char == "1":
            self.__frm_axis_controllers[0].set_cw()

        elif char == "q":
            self.__frm_axis_controllers[0].set_ccw()

        elif char == "2":
            self.__frm_axis_controllers[1].set_cw()

        elif char == "w":
            self.__frm_axis_controllers[1].set_ccw()

        elif char == "3":
            self.__frm_axis_controllers[2].set_cw()

        elif char == "e":
            self.__frm_axis_controllers[2].set_ccw()

        elif char == "4":
            self.__frm_axis_controllers[3].set_cw()

        elif char == "r":
            self.__frm_axis_controllers[3].set_ccw()

        elif char == "5":
            self.__frm_axis_controllers[4].set_cw()

        elif char == "t":
            self.__frm_axis_controllers[4].set_ccw()

        elif char == "6":
            self.__frm_axis_controllers[5].set_cw()

        elif char == "y":
            self.__frm_axis_controllers[5].set_ccw()

        elif char == "s":
            self.__positions.append(self.__current_position)

        elif char == "l":
            for position in self.__positions:
                msg = "Stored position: {}".format(position)
                self.__logger.debug(msg)

        elif char == "g":
            action = Actions.RunStoredPositions
            self.__put_action(action)

    def __frm_update(self):

        self.__update_axis_label()

        self.__update_axis_control_leds()

        self.__update_port_a_inputs()

        # Stop the gripper if it is closed enough.
        if not (2 & self.__port_a_inputs):
            if not self.__frm_axis_controllers[5].is_stopped:
                self.__frm_axis_controllers[5].stop()

    def __frm_on_closing(self):

        self.__is_runing = False

    def __frm_create(self):

        self.__master = Tk()
        self.__master.geometry("600x300")
        self.__master.title("Robko 01")
        self.__master.protocol("WM_DELETE_WINDOW", self.__frm_on_closing)

        # Bind keys.
        self.__master.bind_all("<KeyPress>", self.__frm_key_press)
        self.__master.bind_all("<KeyRelease>", self.__frm_key_release)

        display="Press Any Button, or Press  Key"
        self.__lbl_buttons_state = Label(self.__master, text=display, width=len(display))
        self.__lbl_buttons_state.place(x=33, y=250) # , width= 400, height= 300)

        self.__create_axis_controls()

        self.__create_port_a_outputs()

        self.__create_port_a_inputs()

        self.__create_axis_control_leds()

#endregion

#region Public Methods

    def start(self):

        self.__action_update_timer.start()

        self.__frm_create()
        self.__frm_update_timer.start()

        self.__is_runing = True
        while self.__is_runing:
            self.__master.update()
            self.__frm_update_timer.update()

        self.__master.quit()

    def stop(self):

        self.__is_runing = False

        self.__action_update_timer.stop()

#endregion
