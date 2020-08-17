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

from enum import Enum

class OpCode(Enum):
    """Operation codes."""

#region Enum

    Ping = 1
    """Ping code."""

    Stop = 2
    """Stop robot motion execution."""

    Disable = 3
    """Disable motion of the robot."""

    Enable = 4
    """Enable motion of the robot."""

    Clear = 5
    """Clear robot current position."""

    MoveRelative = 6
    """Move relative to next position."""

    MoveAblolute = 7
    """Move absolute to nex position."""

    DO = 8
    """Write to Digital Outputs."""

    DI = 9
    """Read the digital inputs."""

    IsMoving = 10
    """Return state does one or more axices of the robot are moveing."""

    CurrentPosition = 11
    """Current robot position."""

    MoveSpeed = 12
    """Move in speed mode."""

#endregion

#region Public Static Methods

    @staticmethod
    def to_text(code):
        """Operation code.

        Parameters
        ----------
        code : OpCode
            Operation Code.
        Returns

        -------
        str
            Operation code text.
        """

        text = "Unknown"

        if code == OpCode.Ping.value:
            text = "Ping"

        elif code == OpCode.Stop.value:
            text = "Stop"

        elif code == OpCode.Disable.value:
            text = "Disable"

        elif code == OpCode.Enable.value:
            text = "Enable"

        elif code == OpCode.Clear.value:
            text = "Clear"

        elif code == OpCode.MoveRelative.value:
            text = "Move Relative"

        elif code == OpCode.MoveAblolute.value:
            text = "Move Ablolute"

        elif code == OpCode.DO.value:
            text = "Digitl Outputs"

        elif code == OpCode.DI.value:
            text = "Digital Inputs"

        elif code == OpCode.IsMoving.value:
            text = "Is Moving"

        elif code == OpCode.CurrentPosition.value:
            text = "Current Position"

        elif code == OpCode.MoveSpeed.value:
            text = "Move Speed"

        else:
            text = "Not implemented"

        return text

#endregion
