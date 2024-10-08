#!/usr/bin/env python
# -*- coding: utf8 -*-

"""

Robko 01 - Python Controlftware

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

from robko01.tasks.base_task import BaseTask

from robko01.utils.logger import get_logger

#region File Attributes

__author__ = "Orlin Dimitrov"
"""Author of the file."""

__copyright__ = "Copyright 2020, Orlin Dimitrov"
"""Copyright holder"""

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

__class_name__ = "TaskInputs"
"""Task name."""

#endregion

class TaskInputs(BaseTask):
    """Task template class."""

#region Attributes

#endregion

#region Public Methods

    def start(self):
        """Start the task."""

        self.__logger = get_logger(__name__)
        """Logger
        """

        self._start_cont()

        # Read inputs
        inputs = self._controller.get_inputs()[1]

        # Show it.
        self.__logger.info("Digital Inputs: {}".format(inputs))

#endregion
