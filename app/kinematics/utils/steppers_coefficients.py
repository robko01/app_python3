#!/usr/bin/env python
# -*- coding: utf8 -*-

"""

Robko 01 - Python Control Software

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

from data.j_position import JPosition

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

class SteppersCoefficients():

#region Properties

#endregion

#region Public Methods

    def to_steps(self, j_pos: JPosition):
        """_summary_

        Args:
            S1 (float): Angle [rad]
            S2 (float): Angle [rad]
            S3 (float): Angle [rad]
            S4 (float): Angle [rad]
            S5 (float): Angle [rad]

        Returns:
            tuple: _description_
        """
        sc = SteppersCoefficients()

        return tuple([j_pos.T1 * sc.S1, j_pos.T2 * sc.S2, j_pos.T3 * sc.S3, j_pos.T4 * sc.S4, j_pos.T5 * sc.S5])


    def from_steps(self, j_pos: JPosition):

        return tuple([j_pos.T1 / sc.S1, j_pos.T2 / sc.S2, j_pos.T3 / sc.S3, j_pos.T4 / sc.S4, j_pos.T5 / sc.S5])

#endregion
