
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

class TaskGrasp2(BaseTask):
    """Grasp 2"""

#region Public Methods

    def start(self):
        """Start the task."""

        self._start_cont()

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

#endregion
