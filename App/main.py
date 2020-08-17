#!/usr/bin/env python
# -*- coding: utf8 -*-

"""

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

"""

import sys
import argparse
import signal

from utils.logger import crate_log_file, get_logger

from robot_task_manager import RobotTaskManager
from robot_task_manager import ExecutionMode

from controllers.robot_factory import RobotFactory

__device = None
__logger = None

def main():
    """Main function."""

    global __device, __logger

    # Add signal handler.
    signal.signal(signal.SIGINT, interupt_handler)
    signal.signal(signal.SIGTERM, interupt_handler)

    # Create log.
    crate_log_file()
    __logger = get_logger(__name__)

    # Create parser.
    parser = argparse.ArgumentParser()

    # Add arguments.
    parser.add_argument("--prg", type=str, default="grasp2", help="Builtin program")
    parser.add_argument("--port", type=str, default="COM3", help="Serial port")
    parser.add_argument("--cont", type=str, default="orlin369", help="Controller type")
    parser.add_argument("--step", type=str, default="f", help="Step mode")

    # Take arguments.
    args = parser.parse_args()

    robot = RobotFactory.create_robot(args.port, args.cont)

    if robot is None:
        sys.exit("No controller type specyfied")

    __device = RobotTaskManager(robot)

    if args.step == "f":
        __device.execution_mode = ExecutionMode.Continue
    elif args.step == "t":
        __device.execution_mode = ExecutionMode.Step

    __logger.info("Starting PRG: " + str(args.prg))
    __device.run(args.prg)

def interupt_handler(signum, frame):
    """Interupt handler."""

    global __device, __logger

    if signum == 2:
        __logger.warning("Stoped by interupt.")

    elif signum == 15:
        __logger.warning("Stoped by termination.")

    else:
        __logger.warning("Signal handler called. Signal: {}; Frame: {}".format(signum, frame))

    if __device is not None:
        __device.stop()

if __name__ == "__main__":
    main()

# TODO: Change reposytory and naming, test by virtual env and machine.