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

from App.communicators.serial.communicator import Communicator as SerCom
from App.communicators.ip.communicator import Communicator as IPCom
from App.controllers.orlin369.robko01 import Robko01 as Orko01

from App.controllers.tu_gabrovo.protocol.package_manager import PackageManager as GabkoPM
from App.controllers.tu_gabrovo.robko01 import Robko01 as Gabko01

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

class RobotFactory:
    """Robot factory."""

    @staticmethod
    def create_robot(**kwargs):

        robot = None

        cont = None
        if "cont" in kwargs:
            cont = kwargs["cont"]

        if cont is None:
            raise ValueError("Robot type can not be None.")

        elif cont == "orlin369":

            if "port" in kwargs and "host" not in kwargs:
                name = kwargs["port"]
                robot = Orko01(SerCom(name))

            elif "port" in kwargs and "host" in kwargs:
                if kwargs["host"] is not None or kwargs["host"] is not "":
                    host = kwargs["host"]
                    port = kwargs["port"]
                    robot = Orko01(IPCom(host, port))

        elif cont == "tugab":
            robot = Gabko01(GabkoPM(kwargs))

        else:
            raise ValueError("No controller type specyfyed.")

        return robot
