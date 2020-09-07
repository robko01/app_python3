# Robko01 control application
This document is devoted to the way client software is installed, which communicates with the robot controller.

## Environment
This script is written in Python 3.8.5. To [download](https://www.python.org/downloads/) it please visit official site of the Python and download [3.8.5](https://www.python.org/ftp/python/3.8.5/python-3.8.5.exe)

## Download the application
Download the repository and navigate to the application folder

        $ git clone https://github.com/robko01/app_python3
        $ cd app_python3/
        $ python -m pip install --upgrade pip 
        $ python -m pip install -r requirements.txt

## Dependencies
This script is written in Python 3.8.5.
For the normal operation of the script there are libraries that need to be preinstalled, otherwise the script will not work.

| Name | Version |
|-|:-:|
|pynput | 1.7.1 |
|pyserial | 3.4 |
|six | 1.15.0 |

## Automatic installation

## First run
After installation, the script is ready for operation. This happens in the following way.

        $ python main.py --port <DEVICE COM PORT> --task grasp2

To approach the robot, it will be presented to the computer as a serial port.
The example is marked COM5.
You need to find out which is the correct port for you by using the device manager.
The argument --task serves to indicate which program to execute the robot.