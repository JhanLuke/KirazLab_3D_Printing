import serial
import time
from SerialControl import *
from ConditionControl import *
from Controls import *
from tkinter import *
from PIL import ImageTk, Image




root = Tk()
root.title("3D Printer Controller")
root.iconbitmap("H:/My Drive/3D Print Project/Python/images/KirazLab_logo.ico")

bannerFrame = LabelFrame(root, text="Banner")       # Create frame for banner
bannerFrame.grid(row=0, column=0, sticky="ewns")

banner = ImageTk.PhotoImage(Image.open("H:/My Drive/3D Print Project/Python/images/rsz_kirazlabbanner.png").resize((450, 165), Image.ANTIALIAS))        # Import banner image
bannerLabel = Label(bannerFrame,image=banner)
bannerLabel.grid(row=0, column=0, sticky="ewns")

statusFrame = LabelFrame(root, text="Connection Status")
statusFrame.grid(row=0, column=1, sticky="ewns")

conditionsFrame = LabelFrame(root, text="Condition Control")
conditionsFrame.grid(row=0, column=2, sticky="ewns")

controlFrame = LabelFrame(root, text="Condition Control")
controlFrame.grid(row=1, column=0,columnspan=3, sticky="ewns")


# Checking realtime connection status #################################
def updateStat():
    stat = checkConnection("COM3")
    connectionStatusLabel = Label(statusFrame, text=stat).grid(row=1, column=0, sticky="nsew")
    return port

refreshConnectionButton = Button(statusFrame, text="Check/Refresh Connection", command=updateStat).grid(row=0, column=0, sticky="ew")

def read_ser(num_char=1):
    string = port.read(num_char)
    return string.decode()


def write_ser(cmd):
    cmd = cmd + '\n'
    port.write(cmd.encode())

#######################################################################



# Conditions #####################################################
def setConditions():
    write_ser("M302 S0")
    write_ser("M83")
    canditionsLabel = Label(conditionsFrame, text="Conditions Set!").grid(row=1, column=0,columnspan=2, sticky="ew")

def setF():
    write_ser("G0 F" + str(fSpeedEntry.get()))
    fSpeedLabel = Label(conditionsFrame, text="F set to: " + str(fSpeedEntry.get())).grid(row=3, column=0, columnspan=2, sticky="ew")

def setE():
    write_ser("M92 E" + str(eStepsEntry.get()))
    eSpeedLabel = Label(conditionsFrame, text="E set to: " + str(eStepsEntry.get())).grid(row=6, column=0, columnspan=2, sticky="ew")

fSpeedLabel = Label(conditionsFrame, text="").grid(row=3, column=0, columnspan=2, sticky="ew")
conditionsLabel = Label(conditionsFrame, text="").grid(row=1, column=0,columnspan=2, sticky="ew")

fSpeedButton = Button(conditionsFrame, text="Set F value", command=setF).grid(row=2, column=1, sticky="ew")
eStepsButton = Button(conditionsFrame, text="Set E Value", command=setE).grid(row=5, column=1, sticky="ew")
setConditionsButton = Button(conditionsFrame, text="Set initial conditions", command=setConditions).grid(row=0,column=0,columnspan=2,sticky="ew")

fSpeedEntry = Entry(conditionsFrame, borderwidth=5)
fSpeedEntry.insert(0, "Enter F Value")
fSpeedEntry.grid(row=2, column=0)

eStepsEntry = Entry(conditionsFrame, borderwidth=5)
eStepsEntry.insert(0, "Enter E Value")
eStepsEntry.grid(row=5, column=0)

#########################################################################



def extrudeAmount():
    extrude(erAmountEntry.get())
    eSpeedLabel = Label(controlFrame, text="Extruding:  " + str(erAmountEntry.get()) + " ml").grid(row=3, column=0, sticky="ew")

def retractAmount():
    retract(erAmountEntry.get())
    eSpeedLabel = Label(controlFrame, text="Retracting:  " + str(erAmountEntry.get()) + " ml").grid(row=3, column=0, sticky="ew")

SpeedLabelEmpty = Label(controlFrame, text="                                                            ").grid(row=3, column=0, sticky="ew")

extrudeButton = Button(controlFrame, text="Extrude", command=extrudeAmount).grid(row=0, column=0, sticky="ew")
retractButton = Button(controlFrame, text="Retract", command=retractAmount).grid(row=2, column=0, sticky="ew")

erAmountEntry = Entry(controlFrame, borderwidth=5) # Extrude or Retract amount
erAmountEntry.insert(0, "Enter amount in ml")
erAmountEntry.grid(row=1, column=0,sticky="ew")


root.mainloop()
