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

import math

from Controllers.orlin369.Robko01 import Robko01

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
    