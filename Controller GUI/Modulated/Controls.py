import serial
import time
from SerialControl import *
from tkinter import *




def extrude(value):
    write_ser("G1 E" + value)

def retract(value):
    write_ser("G1 E-" + value)




def calibrateWindow():
    window = Toplevel(root)
    window.title("Calibration")
    window.iconbitmap("H:/My Drive/3D Print Project/Python/images/target.ico")
    warningLabel = Label(window, text="!! Make srue you have at least 12ml !!", fg="red").grid(row=0, column=0,columnspan=3,sticky="ew")
    emptyCalLabel = Label(window, text=" ").grid(row=2, column=0)

    extrudedAmount = Entry(window, borderwidth=5)
    extrudedAmount.insert(0, "Enter Amount Extruded")
    extrudedAmount.grid(row=1, column=2, sticky="ew")

    preCal_eStepsValue = Entry(window, borderwidth=5)
    preCal_eStepsValue.insert(0, "Enter E steps value")
    preCal_eStepsValue.grid(row=1, column=0, sticky="ew")

    def extrudeCalibration():
        write_ser("M302 S0")
        write_ser("M83")
        write_ser("G0 F5")
        write_ser("M92 E" + str(preCal_eStepsValue.get()))
        write_ser("G1 E2")
        extrudeCalLabel = Label(window, text="Extruding 2 ml").grid(row=2, column=0, columnspan=3, sticky="ew")

    def calibrationCalculation():
        new_eStepsValue = float(preCal_eStepsValue.get()) / (float(extrudedAmount.get()) / 2)
        new_eSteps = Label(window, text="Updated E steps value is: " + str(new_eStepsValue)).grid(row=1, column=4,sticky="ew")

    extrudeCalibrationButton = Button(window, text="1. Extrude 2ml", command=extrudeCalibration).grid(row=1, column=1,sticky="ew")
    calibrationButton = Button(window, text="2. Calibrate (new value)", command=calibrationCalculation).grid(row=1,column=3,sticky="ew")


#calibrateButton = Button(statusFrame, text="Calibrate", command=calibrateWindow).pack()