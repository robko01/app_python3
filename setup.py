#!/usr/bin/env python
# -*- coding: utf8 -*-

"""

Robko 01 - Python Controloftware

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

from setuptools import find_packages, setup

#region File Attributes

__author__ = "Orlin Dimitrov"
"""Author of the file."""

__copyright__ = "Copyright 2020, Orlin Dimitrov"
"""Copyright holder"""

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

setup(
    name="robko01",
    packages=find_packages(include=["robko01"]),
    version=__version__,
    description="Robko 01 control library.",
    author=__author__,
    license=__license__,
    install_requires=[],
    setup_requires=[],
    tests_require=["appdirs==1.4.4", "astroid==2.5", "bitstring==3.1.9",\
                   "cffi==1.15.0", "colorama==0.4.4", "cryptography==36.0.1",\
                    "distlib==0.3.1", "ecdsa==0.17.0", "esptool==3.2",\
                    "filelock==3.0.12", "graphviz==0.16", "isort==5.7.0",\
                    "lazy-object-proxy==1.5.2", "mccabe==0.6.1",\
                    "paho-mqtt==1.6.1", "pycparser==2.21", "pygame==2.1.2", "pylint==2.6.0", "pyserial==3.5", "PySide6==6.3.1", "PySide6-Addons==6.3.1", "PySide6-Essentials==6.3.1", "reedsolo==1.5.4", "shiboken6==6.3.1", "six==1.15.0", "toml==0.10.2", "virtualenv==20.4.2", "wrapt==1.12.1"],
    test_suite="",
)
