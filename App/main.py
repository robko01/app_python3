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

import sys
import argparse
import signal

from utils.logger import crate_log_file, get_logger

from tasks.task_manager import TaskManager

from controllers.controller_factory import ControllerFactory

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

__tm = None
__logger = None

def interupt_handler(signum, frame):
    """Interupt handler."""

    global __tm, __logger

    if signum == 2:
        __logger.warning("Stopped by interupt.")

    elif signum == 15:
        __logger.warning("Stopped by termination.")

    else:
        __logger.warning("Signal handler called. Signal: {}; Frame: {}".format(signum, frame))

    if __tm is not None:
        __tm.stop()

def main():
    """Main function."""

    global __tm, __logger

    # Add signal handler.
    signal.signal(signal.SIGINT, interupt_handler)
    signal.signal(signal.SIGTERM, interupt_handler)

    # Create log.
    crate_log_file()
    __logger = get_logger(__name__)

    # Create parser.
    parser = argparse.ArgumentParser()

    # Add arguments.
    parser.add_argument("--task", type=str, default="grasp2", help="Builtin program")
    parser.add_argument("--port", type=str, default="COM3", help="Serial port or TCP port.")
    parser.add_argument("--host", type=str, default=None, help="Host/IP of the robot.")
    parser.add_argument("--cont", type=str, default="orlin369", help="Controller type")
    parser.add_argument("--em", type=str, default="f", help="Step mode")

    # Take arguments.
    args = parser.parse_args()

    controller = ControllerFactory.create_robot(**vars(args))

    if controller is None:
        sys.exit("No controller type specified")

    __tm = TaskManager(controller=controller, task=args.task, em=args.em)
    __tm.start()

if __name__ == "__main__":
    main()
