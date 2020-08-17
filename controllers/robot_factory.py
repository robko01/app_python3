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

from controllers.orlin369.protocol.package_manager import PackageManager as OrkoPM
from controllers.orlin369.robko01 import Robko01 as Orko01

from controllers.tu_gabrovo.protocol.package_manager import PackageManager as GabkoPM
from controllers.tu_gabrovo.robko01 import Robko01 as Gabko01


class RobotFactory:
    """Robot factory."""

    @staticmethod
    def create_robot(c_port, c_type):

        robot = None

        if c_type is None:
            raise ValueError("Robot type can not be None.")

        elif c_type == "orlin369":
            robot = Orko01(OrkoPM(c_port))

        elif c_type == "tugab":
            robot = Gabko01(GabkoPM(c_port))


        else:
            raise ValueError("No controller type specyfyed.")

        return robot
