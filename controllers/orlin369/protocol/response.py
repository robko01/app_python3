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

SUPER - Small Unified Protocol for Extendable Robots

"""

from controllers.orlin369.protocol.frame_indexes import FrameIndexes
from controllers.orlin369.protocol.package_type import PackageType

class Response:
    """Response parser."""

#region Attributes

    __frame = None
    """Frame container."""

    __op_code = 0
    """Operation code."""

    __payload = None
    """Payload container."""

    __size = 0
    """Package size."""

    __status = 0
    """Status flag."""

    __FRAME_STATIC_FIELD_OFFSET = 5
    __FRAME_MIN_PAYLOAD_SIZE = 0
    __FRAME_MAX_PAYLOAD_SIZE = 27

#endregion

#region Constructor

    def __init__(self, frame):
        self.__frame = frame
        self.__parse()

#endregion

#region Destructor

    def __del__(self):
        del self.__frame

#endregion

#region Properties

    @property
    def opcode(self):
        """Operation code.

        Returns
        -------
        int
            Operation code.
        """

        return int(self.__frame[FrameIndexes.OpCode.value])

    @property
    def payload(self):
        """Payload data.

        Returns
        -------
        array
            Payload data.
        """

        return self.__payload

    @property
    def status(self):
        """Status code.

        Returns
        -------
        int
            Status code.
        """

        return int(self.__frame[FrameIndexes.Status.value])

#endregion

#region Private Methods

    def __parse(self):

        if self.is_valid():
            self.__size = int(self.__frame[FrameIndexes.Size.value])

            if (self.__size - 2) > 0:
                self.__payload = []

                for index in range(self.__size - 2):
                    self.__payload.append(self.__frame[index + self.__FRAME_STATIC_FIELD_OFFSET])

    def __is_valid_container(self):
        return self.__frame is not None

    def __is_valid_len(self):
        return len(self.__frame) > 6

    def __is_valid_sentinel(self):
        return self.__frame[FrameIndexes.Sentinel.value] == 0xAA

    def __is_responee(self):
        return self.__frame[FrameIndexes.PackageType.value] == PackageType.Response.value

    def __is_valid_size(self):
        return (int(self.__frame[FrameIndexes.Size.value]) > self.__FRAME_MIN_PAYLOAD_SIZE) and \
                (int(self.__frame[FrameIndexes.Size.value]) < self.__FRAME_MAX_PAYLOAD_SIZE)

#endregion

#region Public Methods

    def is_valid(self):
        """Is valid frame.

        Returns
        -------
        bool
            Is valid frame.
        """

        if self.__is_valid_container() is False:
            return False

        if self.__is_valid_len() is False:
            return False

        state = True

        state = state and self.__is_valid_sentinel()

        state = state and self.__is_responee()

        state = state and self.__is_valid_size()

        return state

    def payload_is(self, payload):
        """Payload validator.

        Parameters
        ----------
        payload : array
            Paylod data.

        Returns
        -------
        Response
            Is the same.
        """

        if self.payload is None:
            return False

        if len(self.payload) <= 0:
            return False

        if payload is None:
            return False

        if payload != self.payload:
            return False

        return True

#endregion
