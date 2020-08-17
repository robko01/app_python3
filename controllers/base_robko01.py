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

class BaseRobko01:
    """Some description that tells you it's abstract,
    often listing the methods you're expected to supply."""

#region Attributes

    _sync_interval = 0.05
    """Sync time."""

    _synchronious = True
    """Sync mode."""

    _time_to_stop = False
    """Time to stop flag."""

    _communicator = None
    """Communicator instance."""

    _timeout = 50

#endregion

#region Properties

    @property
    def time_to_stop(self):
        return self._time_to_stop

    @property
    def synchronious(self):
        """Returns Host URL of the servie.

        Returns
        -------
        str
            Host URL of the servie.
        """
        return self._synchronious

    @synchronious.setter
    def synchronious(self, synchronious):
        """Set Host URL of the service.

        Parameters
        ----------
        host : str
            Host URL of the servie.
        """

        self._synchronious = synchronious

#endregion
