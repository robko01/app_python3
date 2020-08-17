# Robko01 control application
This document is devoted to the way client software is installed, which communicates with the robot controller.

## Environment
This script is written in Python 2.7. To [download](https://www.python.org/downloads/) it please visit ofiicial site of the Python and download [2.7.15](https://www.python.org/downloads/release/python-2715/)

## Download the application
Download the repository and navigate to the application folder

        $ git clone https://github.com/orlin369/Robko01
        $ cd Robko01/OrlinDimitrov/Apps/Python
        $ pip install --upgrade pip 

## Dependencies
This script is written in Python 2.7.
For the normal operation of the script there are libraries that need to be preinstalled, otherwise the script will not work.

| Name | Version |
|-|:-:|
|enum | 0.4.7 |
|future | 0.17.1 |
|iso8601 | 0.1.12 |
|pyserial | 3.4 |
|PyYAML | 3.13 |

## Automatic instalation

To install these libraries, you can use the Python 2.7 package, by calling the following command at the project terminal:

        $ pip install --upgrade -r requirements.txt

## Manual instalation
If you do decide to run dependencies manually, do the following:

        $ pip install enum
        $ pip install pyserial

## First run
After installation, the script is ready for operation. This happens in the following way.

        $ python main.py --port COM5 --prg grasp2

To approach the robot, it will be presented to the computer as a serial port. The example is marked COM5. You need to find out which is the correct port for you by using the device manager.
The argument --prg serves to indicate which program to execute the robot.