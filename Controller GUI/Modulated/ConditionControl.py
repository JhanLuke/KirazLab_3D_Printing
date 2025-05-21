import serial
import time
from SerialControl import *
from tkinter import *




def setInitialConditions():
    write_ser("M302 S0")
    write_ser("M83")

def setFSpeed(value):
    write_ser("G0 F" + str(value))

def setESteps(value):
    write_ser("M92 E" + str(value))


