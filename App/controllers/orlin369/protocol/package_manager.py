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

from controllers.orlin369.protocol.communicator import Communicator
from controllers.orlin369.protocol.package_type import PackageType
from controllers.orlin369.protocol.response import Response

class PackageManager(Communicator):
    """Package manager."""

#region Attributes

    __print_callback = None
    """Print callback."""

#endregion

#region Private Methods

    def __crc(self, payload):
        """Calculate CRC.

        Parameters
        ----------
        payload : bytes array
            Axis steps.

        Returns
        -------
        array
            Odd and Even.
        """

        is_odd = True

        odd = 0
        even = 0

        for char in payload:
            if is_odd:
                odd = odd ^ int(char)
                is_odd = False
            else:
                even = even ^ int(char)
                is_odd = True

        return [int(odd), int(even)]

#endregion

#region Public Methods

    def set_print(self, callback):
        """Set printer function.

        Parameters
        ----------
        callback : pointer to function
            Printer function.
        """

        self.__print_callback = callback

    def request(self, opcode, payload=None):
        """Request to device.

        Parameters
        ----------
        opcode : int
            Operation code.
        payload : byte array
            Payload to device.

        Returns
        -------
        Response
            Response from device.
        """

        # clear the buffer
        req_frame = bytearray()

        # Begin byte.
        req_frame.append(0xAA)

        # Request byte.
        req_frame.append(PackageType.Request.value)

        # Length of the frame.
        if payload is not None:
            req_frame.append(len(payload) + 1)
        else:
            req_frame.append(1)

        # Operation code.
        req_frame.append(opcode)

        if payload is not None:
            # Payload
            for item in payload:
                req_frame.append(int(item))

        # CRC
        crc = self.__crc(req_frame)
        req_frame.append(crc[0])
        req_frame.append(crc[1])

        if self.__print_callback is not None:
            self.__print_callback(req_frame)

        res_frame = self._send_frame(req_frame)
        list_res_frame = list(res_frame)

        if self.__print_callback is not None:
            self.__print_callback(req_frame)

        return Response(list(list_res_frame))

    def response(self, opcode, status, payload=None):
        """Response from device.

        Parameters
        ----------
        opcode : int
            Operation code.
        status : int
            Status code.
        payload : byte array
            Payload to device.

        Returns
        -------
        array bytes
            request to device.
        """

        # clear the buffer
        res_frame = ""

        # Begin byte.
        res_frame += chr(0xAA)

        # Request byte.
        res_frame += chr(PackageType.Response)

        # Length of the frame.
        if payload is not None:
            res_frame += chr(len(payload) + 2)
        else:
            res_frame += chr(2)

        # Operation code.
        res_frame += chr(opcode.value)

        # Status code
        res_frame += chr(status.value)

        if payload is not None:
            # Payload
            res_frame += payload

        # CRC
        res_frame += self.__crc(res_frame)

        return res_frame

#endregion
