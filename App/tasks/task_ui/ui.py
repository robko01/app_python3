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

import queue
from tkinter import *
from tkinter.messagebox import askyesno
from tkinter.ttk import Notebook

from tasks.task_ui.actions import Actions
from tasks.task_ui.axis_action_controller import *
from tasks.task_ui.led import LedStatus
from tasks.task_ui.led import LedShape
from tasks.task_ui.led import LED

from utils.logger import get_logger
from utils.thread_timer import ThreadTimer
from utils.timer import Timer

from kinematics.data.c_position import CPosition
from kinematics.data.j_position import JPosition
from kinematics.data.steppers_coefficients import SteppersCoefficients
from kinematics.kinematics import Kinematics

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

    __frm_tab_man = None
    """Form tab manual.
    """

    __frm_tab_auto = None
    """Forma tab auto.
    """

    __frm_port_a_input_leds = []
    """Port A input LEDs.
    """

    __frm_port_a_output_chk = []
    """Port A outputs Checks.
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

    __current_speed = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    """Axis speeds.
    """

    __current_position = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    """Current end-efector position.
    """

    __axis_states = 0
    """Axis action states.
    """

    __port_a_inputs = 0
    """Port A inputs.
    """

    __port_a_outputs = 0
    """Port A outputs.
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

        # Kinematics
        self.__kin = Kinematics()
        self.__sc = SteppersCoefficients()

#endregion

#region Private Methods (Action Control)

    def __put_action(self, action):

        self.__actions_queue.put(action)

    def __do_action(self, action):

        if action == Actions.NONE:
            pass

        if action == Actions.UpdateSpeeds:
            self.__controller.move_speed(self.__current_speed)

        elif action == Actions.UpdateOutputs:
            self.__controller.set_outputs(self.__port_a_outputs)

        elif action == Actions.ClearController:
            self.__controller.clear()

        elif action == Actions.ResetController:
            pass

        elif action == Actions.DoTest1:
            self.__controller.move_absolute([200, 100, 200, 100, 200, 100, 0, 0, 0, 0, 0, 0])

        elif action == Actions.DoTest2:
            self.__controller.move_absolute([0, 100, 0, 100, 0, 100, 0, 0, 0, 0, 0, 0])

    def __action_timer_cb(self):

        self.__axis_states = self.__controller.is_moving()
        self.__port_a_inputs = self.__controller.get_inputs()
        self.__current_position = self.__controller.current_position()

        if not self.__actions_queue.empty():
            action = self.__actions_queue.get()
            self.__do_action(action)

#endregion

#region Private Methods (Axices CB)

    def __axis_0(self, speed):

        self.__current_speed[1] = speed * -1

        self.__put_action(Actions.UpdateSpeeds)

    def __axis_1(self, speed):

        self.__current_speed[3] = speed * -1

        self.__put_action(Actions.UpdateSpeeds)

    def __axis_2(self, speed):

        self.__current_speed[5] = speed
        self.__current_speed[11] = speed * -1

        self.__put_action(Actions.UpdateSpeeds)

    def __axis_3(self, speed):

        self.__current_speed[7] = speed * -1
        self.__current_speed[9] = speed

        self.__put_action(Actions.UpdateSpeeds)

    def __axis_4(self, speed):

        self.__current_speed[7] = speed
        self.__current_speed[9] = speed

        self.__put_action(Actions.UpdateSpeeds)

    def __axis_5(self, speed):

        self.__current_speed[11] = speed

        self.__put_action(Actions.UpdateSpeeds)

#endregion

#region Private Methods (Keyboard Events)

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

#endregion

#region Private Methods (Form)

    def __create_tabs(self):

        self.notebook = Notebook(self.__master)

        self.__frm_tab_man = Frame(self.notebook)
        self.notebook.add(self.__frm_tab_man, text="Manual")

        self.__frm_tab_auto = Frame(self.notebook)
        self.notebook.add(self.__frm_tab_auto, text="Auto")        

        self.notebook.pack(expand=1, fill ="both")


    def __mnu_clear_controller(self):

        answer = askyesno(title="Clear axis positions", message="Are you sure you want to clear the axis positions?")
        if answer:
            self.__put_action(Actions.ClearController)

    def __mnu_reset_controller(self):

        answer = askyesno(title="Reset robot controller", message="Are you sure you want to reset the robot controller?")
        if answer:
            self.__put_action(Actions.ResetController)

    def __mnu_enable_kbc(self):

        value = self.__bv_enable_kbc.get()

        if value:
            # Bind keys.
            self.__bid_press = self.__master.bind_all("<KeyPress>", self.__frm_key_press)
            self.__bid_release = self.__master.bind_all("<KeyRelease>", self.__frm_key_release)

        else:
            # Unbind keys.
            self.__master.unbind("<KeyPress>", self.__bid_press)
            self.__master.unbind("<KeyRelease>", self.__bid_release)

    def __mnu__do_test_1(self):

        self.__put_action(Actions.DoTest1)

    def __mnu__do_test_2(self):

        self.__put_action(Actions.DoTest2)

    def __create_menu_bar(self):

        donothing = None

        # Menu bar.
        menu_bar = Menu(self.__master)

        # First menu block.
        filemenu = Menu(menu_bar, tearoff=0)
        filemenu.add_command(label="New", command=donothing)
        filemenu.add_command(label="Open", command=donothing)
        filemenu.add_command(label="Save", command=donothing)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.__frm_on_closing)
        menu_bar.add_cascade(label="File", menu=filemenu)

        # Second menu block.
        controller_menu = Menu(menu_bar, tearoff=0)
        controller_menu.add_command(label="Clear", command=self.__mnu_clear_controller)
        controller_menu.add_command(label="Reset", command=self.__mnu_reset_controller)
        
        self.__bv_enable_kbc = BooleanVar()
        self.__bv_enable_kbc.set(False)
        controller_menu.add_checkbutton(
            label="Enable Keyboard Control",
            onvalue=1,
            offvalue=0,
            variable=self.__bv_enable_kbc,
            command=self.__mnu_enable_kbc)
        # controller_menu.add_command(label="Do Test 1", command=self.__mnu__do_test_1)
        # controller_menu.add_command(label="Do Test 2", command=self.__mnu__do_test_2)
        menu_bar.add_cascade(label="Controller", menu=controller_menu)

        # Third menu block.
        helpmenu = Menu(menu_bar, tearoff=0)
        helpmenu.add_command(label="About", command=donothing)
        menu_bar.add_cascade(label="Help", menu=helpmenu)

        # Add the menu.
        self.__master.config(menu=menu_bar)


    def __update_port_a_outputs(self):

        value = 0

        for bit in range(0, 8):
            value += self.__frm_port_a_output_chk[bit].get()

        self.__port_a_outputs = value
        self.__put_action(Actions.UpdateOutputs)

    def __create_port_a_outputs(self):

        # Create the frame.
        lbl_frame = LabelFrame(self.__frm_tab_man, text="DO on port A")

        # Create the check boxes.
        for index in range(0, 8):

            # Bit wight.
            bit_weight = (2**index)

            # Create the check box.
            var = IntVar()
            check = Checkbutton(lbl_frame, variable=var, onvalue=bit_weight, offvalue=0, command=self.__update_port_a_outputs)
            check.grid(row=0, column=index)
            self.__frm_port_a_output_chk.append(var)

        # Place the frame.
        lbl_frame.place(x=33, y=200)


    def __update_port_a_inputs(self):

        if len(self.__frm_port_a_input_leds) == 8:
            led_index = 7
            for index in range(0, 8):
                if (2**index) & self.__port_a_inputs:
                    self.__frm_port_a_input_leds[led_index].turnoff()
                else:
                    self.__frm_port_a_input_leds[led_index].turnon()
                led_index -= 1

    def __create_port_a_inputs(self):

        # Create the frame.
        lbl_frame = LabelFrame(self.__frm_tab_man, text="DI on port A")

        led_w = 20
        led_h = 20

        for index in range(0, 8):

            led = LED(lbl_frame, shape=LedShape.ROUND, status=LedStatus.OFF,
                width=led_w, height=led_h, appearance=RAISED,
                blink=0, bd=1, outline="")
            led.frame.grid(row=0, column=index)

            self.__frm_port_a_input_leds.append(led)

        # Place the frame.
        lbl_frame.place(x=350, y=200)


    def __update_axis_control_leds(self):

        if len(self.__frm_axis_control_leds) == 6:
            for index in range(0, 6):
                if (2**index) & self.__axis_states:
                    self.__frm_axis_control_leds[index].turnon()
                else:
                    self.__frm_axis_control_leds[index].turnoff()

    def __create_axis_control_leds(self):

        # Create the frame.
        lbl_frame = LabelFrame(self.__frm_tab_man, text="Axis control LEDs")

        led_w = 20
        led_h = 20

        for index in range(0, 6):

            led = LED(lbl_frame, shape=LedShape.ROUND, status=LedStatus.OFF,
                width=led_w, height=led_h, appearance=RAISED,
                blink=0, bd=1, outline="")
            led.frame.grid(row=0, column=index)

            self.__frm_axis_control_leds.append(led)

        # Place the frame.
        lbl_frame.place(x=350, y=250)


    def __update_slider_speed(self, event):

        for index in range(0, 6):
            self.__frm_axis_controllers[index].speed = self.__sldr_speed.get()

    def __update_axis_label(self):

        for index in range(0, 6):
            text = "P: {}\nV: {}".format(self.__current_position[index*2], self.__current_position[index*2 + 1])
            self.__frm_axis_labels[index].config(text=text)

    def __create_axis_controls(self):

        w_size = 10
        h_size = 10

        # Create the frame.
        frame = Frame(self.__frm_tab_man)

        empty_text = "P: {}\nV: {}".format(0, 0)

        fields = {
            "cw":[
                {
                    "text": "Base CW",
                    "press": lambda event: self.__frm_axis_controllers[0].set_cw(),
                    "release": lambda event: self.__frm_axis_controllers[0].stop()
                },
                {
                    "text": "Shoulder UP",
                    "press": lambda event: self.__frm_axis_controllers[1].set_cw(),
                    "release": lambda event: self.__frm_axis_controllers[1].stop()
                },
                {
                    "text": "Elbow UP",
                    "press": lambda event: self.__frm_axis_controllers[2].set_cw(),
                    "release": lambda event: self.__frm_axis_controllers[2].stop()
                },
                {
                    "text": "P UP",
                    "press": lambda event: self.__frm_axis_controllers[3].set_cw(),
                    "release": lambda event: self.__frm_axis_controllers[3].stop()
                },
                {
                    "text": "R CW",
                    "press": lambda event: self.__frm_axis_controllers[4].set_cw(),
                    "release": lambda event: self.__frm_axis_controllers[4].stop()
                },
                {
                    "text": "Gripper OPEN",
                    "press": lambda event: self.__frm_axis_controllers[5].set_cw(),
                    "release": lambda event: self.__frm_axis_controllers[5].stop()
                },
            ],
            "ccw":[
                {
                    "text": "Base CCW",
                    "press": lambda event: self.__frm_axis_controllers[0].set_ccw(),
                    "release": lambda event: self.__frm_axis_controllers[0].stop()
                },
                {
                    "text": "Shoulder DOWN",
                    "press": lambda event: self.__frm_axis_controllers[1].set_ccw(),
                    "release": lambda event: self.__frm_axis_controllers[1].stop()
                },
                {
                    "text": "Elbow DOWN",
                    "press": lambda event: self.__frm_axis_controllers[2].set_ccw(),
                    "release": lambda event: self.__frm_axis_controllers[2].stop()
                },
                {
                    "text": "P DOWN",
                    "press": lambda event: self.__frm_axis_controllers[3].set_ccw(),
                    "release": lambda event: self.__frm_axis_controllers[3].stop()
                },
                {
                    "text": "R CCW",
                    "press": lambda event: self.__frm_axis_controllers[4].set_ccw(),
                    "release": lambda event: self.__frm_axis_controllers[4].stop()
                },
                {
                    "text": "Gripper CLOSE",
                    "press": lambda event: self.__frm_axis_controllers[5].set_ccw(),
                    "release": lambda event: self.__frm_axis_controllers[5].stop()
                }
            ]
        }

        buttons_cw = []
        buttons_ccw = []

        for index in range(0, 6):

            self.__frm_axis_labels.append(Label(frame, text=empty_text))
            self.__frm_axis_labels[index].grid(row=0, column=index, ipadx=h_size, ipady=w_size, sticky="ew")

            buttons_cw.append(Button(frame, text=fields["cw"][index]["text"]))
            buttons_cw[index].bind("<ButtonPress-1>", fields["cw"][index]["press"])
            buttons_cw[index].bind("<ButtonRelease-1>", fields["cw"][index]["release"])
            buttons_cw[index].grid(row=1, column=index, ipadx=h_size, ipady=w_size, sticky="ew")

            buttons_ccw.append(Button(frame, text=fields["ccw"][index]["text"]))
            buttons_ccw[index].bind("<ButtonPress-1>", fields["ccw"][index]["press"])
            buttons_ccw[index].bind("<ButtonRelease-1>", fields["ccw"][index]["release"])
            buttons_ccw[index].grid(row=2, column=index, ipadx=h_size, ipady=w_size, sticky="ew")

        # Place the frame.
        frame.place(x=33, y=33)

    def __create_axis_speed(self):

        lbl_frame = LabelFrame(self.__frm_tab_man, text="Axises speed")

        self.__sldr_speed = Scale(lbl_frame, from_=20, to=150, orient="horizontal", command=self.__update_slider_speed)
        self.__sldr_speed.grid(row=0, column=0, sticky="ew")
        self.__sldr_speed.set(100)

        lbl_frame.place(x=33, y=250) # , width= 400, height= 300)


    def __update_cartesian_pos_lbl(self):

        j1 = self.__current_position[0] / self.__sc.T1const
        j2 = self.__current_position[2] / self.__sc.T2const
        j3 = self.__current_position[4] / self.__sc.T3const
        j4 = self.__current_position[6] / self.__sc.T4const
        j5 = self.__current_position[8] / self.__sc.T5const
        d_pos = self.__kin.forward_from_scale(j1, j2, j3, j4, j5)
        x = d_pos[0]
        y = d_pos[1]
        z = d_pos[2]
        p = d_pos[3]
        r = d_pos[4]
        message = "X: {0:.2f} P: {3:.2f}\nY: {1:.2f} R: {3:.2f}\nZ: {2:.2f}".format(x, y, z, p, r)
        self.__lbl_pos.config(text=message)
    
    def __create_cartesian_pos_lbl(self):
        text_pos = "-------------------"
        self.__lbl_pos = Label(self.__master, text=text_pos, width=len(text_pos))
        self.__lbl_pos.place(x=33, y=350) # , width= 400, height= 300)


    def __frm_update(self):

        self.__update_axis_label()

        self.__update_axis_control_leds()

        self.__update_port_a_inputs()

        # Stop the gripper if it is closed enough.
        if (1 & self.__port_a_inputs):
            if self.__frm_axis_controllers[5].direction == -1:
                self.__frm_axis_controllers[5].stop()
        
        # if (2 & self.__port_a_inputs):
        #     if self.__frm_axis_controllers[5].direction == -1:
        #         self.__frm_axis_controllers[5].stop()
        
        self.__update_cartesian_pos_lbl()

    def __frm_on_closing(self):

        self.__is_runing = False

    def __frm_create(self):

        self.__master = Tk()
        self.__master.geometry("700x500")
        self.__master.title("Robko 01")
        self.__master.protocol("WM_DELETE_WINDOW", self.__frm_on_closing)

        display="Press Any Button, or Press  Key"
        self.__lbl_buttons_state = Label(self.__master, text=display, width=len(display))
        self.__lbl_buttons_state.place(x=33, y=250) # , width= 400, height= 300)

        self.__create_menu_bar()

        self.__create_tabs()

        self.__create_axis_controls()

        self.__create_port_a_outputs()

        self.__create_port_a_inputs()

        self.__create_axis_control_leds()

        self.__create_axis_speed()

        self.__create_cartesian_pos_lbl()

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
