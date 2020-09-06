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

import math

from Controllers.orlin369.Robko01 import Robko01

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

class Kinematics(Robko01):

    # Страница 67 таблица 190
    __H  = 190
    
    # Не я знам от къде идва
    # Константата трябва да се редактира!!!
    __C  = 20
    
    # Не я знам от къде идва
    # Константата трябва да се редактира!!!
    __LG = 30
    
    # Не я знам от къде идва
    # Константата трябва да се редактира!!!
    __R1 = 40
    
    # Страница 80 фигура 4.12
    # Константата трябва да се редактира!!!
    __L1 = 40
    
    # Страница 80 фигура 4.12
    # Константата трябва да се редактира!!!
    __L2 = 40

    def __sign(self, value):
        sign = 1.0
        if(value > 0):
            sign = 1.0
        elif(value < 0):
            sign = -1.0
        else:
            sign = 0.0
    
            return sign
    
    def iverse_kinematic(self, X0, Y0, Z0, P0, R0):
        
        RR = 0.0
        LF = 0.0
        RM = 0.0
        GA = 0.0
        AL = 0.0
        
        if (Z0 < 0):
            Z0 = 0
            
        if (Z0 < 300 and X0 < 0):
            X0 = 100
    
        RR = math.sqrt(X0 * X0 + Y0 * Y0)
        LF = 2 * self.__L1 + self.__LG
        
        if (Z0 == self.__H):
            RM = LF
        elif (Z0 == 0):
            RM = math.sqrt((LF * LF) - (self.__H * self.__H))
        else:
            RM = math.sqrt((LF * LF) - ((self.__H - Z0) * (self.__H - Z0)))
            
        if (RR > RM):
            RR = RM
            
        P0 = P0 / self.__C
        R0 = R0 / self.__C
        R0 = RR - self.__LG * math.cos(P0)
        Z0 = self.__H - Z0 - self.__LG * math.sin(P0)
        
        if (R0 == 0):
            GA = self.__sign(Z0) * math.PI / 2
        else:
            GA = math.atan(Z0 / R0)
        
        AL = math.sqrt((R0 * R0) + (Z0 * Z0)) / 2
        AL = math.atan(math.sqrt((self.__L1 * self.__L1) - (AL * AL)) / AL)
    
        if (X0 == 0):
            T1 = self.__sign(Y0) * math.PI / 2
        else:
            T1 = math.atan(Y0 / X0)
            
        T2 = GA - AL
        T3 = GA + AL
        T4 = P0 + R0 + self.__R1 * T1
        T5 = P0 - R0 - self.__R1 * T1
        
        return (T1, T2, T3, T4, T5)
        
    def rights_kinematic(self, T1, T2, T3, T4, T5):
    
        RP = 0.0
    
        PP = (T4 + T5) / 2
        RR = (T4 - T5) / 2 - self.__R1 * T1
        RP = self.__L1 * math.cos(T2) + self.__L2 * math.cos(T3) + self.__LG * math.cos(PP)
        XX = RP * math.cos(T1)
        YY = RP * math.sin(T1)
        ZZ = self.self.__H - self.__L1 * math.sin(T2) - self.__L2 * math.sin(T3) - self.__LG * math.sin(PP)
        PP = PP * self.__C
        RR = RR * self.__C
        
        return (XX, YY, ZZ, PP, RR)
    