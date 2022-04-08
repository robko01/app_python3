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

class CPosition():

#region Attributes

    __x = 0.0

    __y = 0.0

    __z = 0.0

    __p = 0.0

    __r = 0.0

#endregion

#region Properties

    @property
    def X(self):
        return self.__x

    @X.setter
    def X(self, value):
        self.__x = value
        self.__update()

    @property
    def Y(self):
        return self.__y

    @Y.setter
    def Y(self, value):
        self.__y = value
        self.__update()

    @property
    def Z(self):
        return self.__z

    @Z.setter
    def Z(self, value):
        self.__z = value
        self.__update()

    @property
    def P(self):
        return self.__p

    @P.setter
    def P(self, value):
        self.__p = value
        self.__update()

    @property
    def R(self):
        return self.__r

    @R.setter
    def R(self, value):
        self.__r = value
        self.__update()

#endregion

#region Constructor

    def __init__(self, **kwargs):

        if "X" in kwargs:
            self.X = kwargs["X"]

        if "Y" in kwargs:
            self.Y = kwargs["Y"]

        if "Z" in kwargs:
            self.Z = kwargs["Z"]

        if "P" in kwargs:
            self.P = kwargs["P"]

        if "R" in kwargs:
            self.R = kwargs["R"]

    def __str__(self):

        message = "X = {:3.2f}\r\nY = {:3.2f}\r\nZ = {:3.2f}\r\nP = {:3.2f}\r\nR = {:3.2f}".format(self.X, self.Y, self.Z, self.P, self.R)

        return message

    __repr__ = __str__

#endregion

#region Private Methods

    def __update(self):

        pass

#endregion
