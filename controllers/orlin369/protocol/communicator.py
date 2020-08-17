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

import time

import serial

class Communicator:
    """This class is dedicated to work with the serial interface."""

#region Attributes

    __port = None
    """Serial port."""

    __timeout = 5
    """Timeout in second."""

    __baudrate = 115200 #921600
    """Baud rate."""

#endregion

#region Constructor

    def __init__(self, name):
        """Move axis in absolute mode.

        Parameters
        ----------
        name : str
            Serial port name.
        """

        self.__port = serial.Serial(name, self.__baudrate)

#endregion

#region Protected Methods

    def _send(self, payload):

        self.__port.write(payload)

    def _receive(self):

        frame = None
        wait = 0.1
        times = 0

        while True:
            size = self.__port.inWaiting()
            if size > 0:
                frame = self.__port.read(size)
                break

            times += wait
            time.sleep(wait)

            if times > self.__timeout:
                raise Exception("Time out hase ocured in Communicator.")

        return frame

    def _send_frame(self, req_frame):

        if self.__port.isOpen() is False:
            raise Exception("Port is not opened on level Communicator.")

        #self._open()
        self._send(req_frame)
        res_frame = None
        res_frame = self._receive()
        #self._close()
        return res_frame

#endregion

#region Public Methods

    def connect(self):
        """Connect to the device."""

        if self.__port.isOpen() is False:

            self.__port.timeout = self.__timeout
            self.__port.setDTR(False)
            self.__port.setRTS(False)
            self.__port.open()

    def disconnect(self):
        """Dissconnect from device."""

        if self.__port.isOpen() is True:

            self.__port.setDTR(False)
            self.__port.setRTS(False)
            self.__port.close()

    def reset(self):
        """Reset target device."""

        if self.__port.isOpen() is False:
            raise Exception("Port is not opened on level Communicator.")

        self.__port.setDTR(False)
        self.__port.setRTS(False)
        time.sleep(0.001)
        self.__port.setDTR(True)
        self.__port.setRTS(True)
        time.sleep(0.001)
        self.__port.setDTR(False)
        self.__port.setRTS(False)
        time.sleep(self.__timeout)

#endregion
