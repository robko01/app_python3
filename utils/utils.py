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

from struct import unpack

def scale(value, in_min, in_max, out_min, out_max):
    """Scale value.

    Parameters
    ----------
    value : float
        Value for scaling.
    in_min : float
        Input value minimum.
    in_max : float
        Input value maximum.
    out_min : float
        Output value minimum.
    out_max : float
        Output value maximum.

    Returns
    -------
    float
        Scaled value.
    """

    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def scale_speeds(position, speed):
    """Proportional speed scales.

    Parameters
    ----------
    position : array
        Positions.
    speed : float
        Maximum speed.

    Returns
    -------
    array
        Scaled speed values.
    """

    positions = []

    for index in range(len(position)):

        if index % 2 == 0:
            positions.append(position[index])

    max_pos = max(positions)

    speeds = []

    for index in range(len(positions)):

        if max_pos == 0:
            speeds.append(100)

        else:
            speeds.append(abs(scale(positions[index], 0, max_pos, 0, speed)))

    pos_index = 0
    speed_index = 0

    for index in range(len(position)):

        if index % 2 == 0:
            position[index] = positions[pos_index]
            pos_index += 1

        else:
            position[index] = speeds[speed_index]
            speed_index += 1

    return position

def int_to_bin(in_value):
    """Convert Integer to Binary.

    Parameters
    ----------
    in_value : int
        Input value.

    Returns
    -------
    str
        String binary format.
    """

    value = unpack("B", in_value)
    value = int(value[0])
    value = "{0:08b}".format(value)

    return value
