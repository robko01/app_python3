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

class StatusCode(Enum):
    """Status codes."""

#region Enum

    Ok = 1
    """When everything is OK."""

    Error = 2
    """When error occurred."""

    Busy = 3
    """When busy in other operation."""

    TimeOut = 4
    """Then time for the operation has timed out."""

#endregion

#region Static Public Methods

    @staticmethod
    def to_text(status):
        """Status code.

        Parameters
        ----------
        code : StatusCode
            Status Code.
        Returns

        -------
        str
            Status code text.
        """

        text = ""

        if status == StatusCode.Ok.value:
            text = "OK"

        elif status == StatusCode.Error.value:
            text = "Error"

        elif status == StatusCode.Busy.value:
            text = "Busy"

        elif status == StatusCode.TimeOut.value:
            text = "TimeOut"

        return text

#endregion
