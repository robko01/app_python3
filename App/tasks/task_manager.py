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

from utils.logger import get_logger

from tasks.task_kbd.task_kbd import TaskKbd
from tasks.task_cmd.task_cmd import TaskCmd
from tasks.task_grasp_1.task_grasp_1 import TaskGrasp1
from tasks.task_grasp_2.task_grasp_2 import TaskGrasp2
from tasks.task_grasp_3.task_grasp_3 import TaskGrasp3
from tasks.task_inputs.task_inputs import TaskInputs

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

class TaskManager:
    """This class handles the robot tasks in nice procedure way."""

#region Attributes

    __logger = None
    """Logger"""

    __controller = None
    """Robot controller."""

    __execution_mode = ExecutionMode.Pause
    """Mode of execution."""

    __task_name = ""
    """Program name."""

    __task = None
    """The task."""

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

    def __init__(self, **kwargs):
        """Constructor

        Parameters
        ----------
        kwargs : mixed
            Key wards arguments.
        """

        self.__logger = get_logger(__name__)

        if "controller" in kwargs:
            self.__controller = kwargs["controller"]

        if "task" in kwargs:
            self.__set_task(kwargs["task"])

        if "em" in kwargs:
            self.__execution_mode = kwargs["em"]

#endregion

#region Private Methods

    def __set_task(self, task_name):
        """Set execution mode.

        Parameters
        ----------
        program : str
            Program name.
        """

        self.__task_name = task_name

        if self.__task_name == "cmd":
            self.__task = TaskCmd(cont=self.__controller, em=self.__execution_mode)

        elif self.__task_name == "grasp1":
            self.__task = TaskGrasp1(cont=self.__controller, em=self.__execution_mode)

        elif self.__task_name == "grasp2":
            self.__task = TaskGrasp2(cont=self.__controller, em=self.__execution_mode)

        elif self.__task_name == "grasp3":
            self.__task = TaskGrasp3(cont=self.__controller, em=self.__execution_mode)

        elif self.__task_name == "inputs":
            self.__task = TaskInputs(cont=self.__controller, em=self.__execution_mode)

        elif self.__task_name == "kb":
            self.__task = TaskKbd(cont=self.__controller, em=self.__execution_mode)

        elif  self.__task_name is not None:
            self.__logger.error("No program selected")

        else:
            self.__logger.error("No program selected")

#endregion

#region Public Methods

    def start(self):
        """Start the task."""

        if self.__task is not None:
            self.__logger.info("Starting task: {}".format(self.__task_name))
            self.__task.start()

    def stop(self):
        """Stop the task."""

        if self.__task is not None:
            self.__logger.info("Stopping task: {}".format(self.__task_name))
            self.__task.stop()

#endregion
