import serial
import time
from tkinter import *
from PIL import ImageTk, Image

# ============================== GUI WINDOW SETUP ==============================

# Create main application window
root = Tk()
root.title("3D Printer Controller")

# ---------------- ICON SETUP ----------------
# NOTE: Change the path below to the icon file on your system (Windows-only feature)
try:
    root.iconbitmap("images/KirazLab_logo.ico")  # Example relative path
except Exception as e:
    print(f"Icon load failed: {e}")  # Will fail silently on macOS/Linux

# ---------------- BANNER IMAGE ----------------
# NOTE: Change the path below to your banner image file
try:
    banner_img = Image.open("images/rsz_kirazlabbanner.png").resize((600, 225), Image.ANTIALIAS)
    banner = ImageTk.PhotoImage(banner_img)
    bannerLabel = Label(root, image=banner)
    bannerLabel.grid(row=0, column=0, sticky="ewns")
except Exception as e:
    print(f"Banner image load failed: {e}")

# ============================== STATUS FRAME ==============================

# Frame for connection status and control commands
statusFrame = LabelFrame(root, text="Connection Status and Command")
statusFrame.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

# ============================== SERIAL CONNECTION SETUP ==============================

# Configuration for serial communication
MAX_BUFF_LEN = 255       # Maximum buffer length (currently unused but reserved)
SETUP = False            # Connection flag
port = None              # Global variable to hold the serial port object

# NOTE: Change this to the correct port for your printer (e.g., 'COM3' on Windows, '/dev/ttyUSB0' on Linux/Mac)
SERIAL_PORT = "COM3"
BAUD_RATE = 115200

# Try connecting to the serial port in a loop (blocks GUI, not ideal)
prev = time.time()
while not SETUP:
    try:
        port = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    except serial.SerialException:  # Catch only serial-related errors
        if time.time() - prev > 2:  # Limit message frequency
            print("No serial detected, please plug in the 3D printer.")
            prev = time.time()

    if port is not None:
        SETUP = True
        # Show connection success in the GUI
        Label(statusFrame, text=f"Connected to {SERIAL_PORT}!", fg="green").grid(
            row=0, column=0, columnspan=2, sticky="ew"
        )


def sendCommand():
    write_ser(commandValue.get())
    commandLabel = Label(statusFrame, text=commandValue.get()).grid(row=4, column=0,columnspan=2,sticky="ew")


def homeAxis():
    write_ser("G28")
    homeLabel = Label(statusFrame, text="Homing Axis").grid(row=4, column=0,columnspan=2,sticky="ew")


def read_ser(num_char=1):
    string = port.read(num_char)
    return string.decode()


def write_ser(cmd):
    cmd = cmd + '\n'
    port.write(cmd.encode())

commandValue = Entry(statusFrame, borderwidth=5)
commandValue.insert(0, "Enter Command")
commandValue.grid(row=3, column=0)

homeButton = Button(statusFrame, text="Home Axis", command=homeAxis).grid(row=2, column=0,columnspan=2, sticky="ew")
commandButton = Button(statusFrame, text="Send Command", command=sendCommand).grid(row=3, column=1, sticky="ew")



### end - Frame - Connection Status and Command



########################################################################################################



### Frame - Variables and Conditions

variableFrame = LabelFrame(root, text="Variables and Conditions", padx=25, pady=25)
variableFrame.grid(row=1, column=0, sticky="ewns")

enterFLabel = Label(variableFrame, text="Enter F Value: ").grid(row=1, column=0, sticky="ew")
enterELabel = Label(variableFrame, text="Enter E Value: ").grid(row=2, column=0, sticky="ew")

fSpeedValue = Entry(variableFrame, borderwidth=5)
fSpeedValue.grid(row=1, column=1)

eStepsValue = Entry(variableFrame, borderwidth=5)
eStepsValue.grid(row=2, column=1)

setConLabel = Label(variableFrame, text="Initial Conditions Not Set!").grid(row=0, column=3, sticky="ew")

def setInitialConditions():
    write_ser("M302 S0")
    write_ser("M83")
    setLabel = Label(variableFrame, text="Initial Conditions Set!").grid(row=0, column=3, sticky="ew")


def fSpeed():
    write_ser("G0 F" + fSpeedValue.get())
    fSpeedLabel = Label(variableFrame, text="F set to " + fSpeedValue.get()).grid(row=1, column=3, sticky="ew")


def eSteps():
    write_ser("M92 E" + eStepsValue.get())
    eStepsLabel = Label(variableFrame, text="E set to " + eStepsValue.get()).grid(row=2, column=3, sticky="ew")

initialConditions = Button(variableFrame, text="Set initial conditions", command=setInitialConditions).grid(row=0,column=0,columnspan=3,sticky="ew")
fSpeedButton = Button(variableFrame, text="Set F value", command=fSpeed).grid(row=1, column=2, sticky="ew")
eStepsButton = Button(variableFrame, text="Set E Value", command=eSteps).grid(row=2, column=2, sticky="ew")

### end - Frame - Variables and Conditions



########################################################################################################



### Frame - Extrusion Control

extrudeFrame = LabelFrame(root, text="Extrusion control", padx=25, pady=25)
extrudeFrame.grid(row=1, column=1, sticky="ewns")

extrudeValue = Entry(extrudeFrame, borderwidth=5)
extrudeValue.insert(0, "Amount")
extrudeValue.grid(row=1, column=0, sticky="ew")

emptyLabel = Label(extrudeFrame, text="").grid(row=3, column=0, sticky="ew")

def extrude():
    write_ser("G1 E" + extrudeValue.get())
    extrudeLabel = Label(extrudeFrame, text="Extruding " + extrudeValue.get() + " ml").grid(row=3, column=0,sticky="ew")


def retract():
    write_ser("G1 E-" + extrudeValue.get())
    retractLabel = Label(extrudeFrame, text="Retracting " + extrudeValue.get() + " ml").grid(row=3, column=0,sticky="ew")

extrudeButton = Button(extrudeFrame, text="Extrude", command=extrude).grid(row=0, column=0, sticky="ew")
retractButton = Button(extrudeFrame, text="Retract", command=retract).grid(row=2, column=0, sticky="ew")

### end - Frame - Extrusion Control



########################################################################################################



### Frame - Lineer Movement

global xCoord
global yCoord
global zCoord

xCoord = 0
yCoord = 0
zCoord = 0

movementFrame = LabelFrame(root, text="Lineer Movement", padx=25, pady=25)
movementFrame.grid(row=0, column=2, sticky="ewns")

movementStepValue = Entry(movementFrame, borderwidth=5)
movementStepValue.insert(0, "Enter Step")
movementStepValue.grid(row=1, column=1)

def lineerXMove(xCoord):
    write_ser("G0 X" + movementStepValue.get())
    xCoord = xCoord + float(movementStepValue.get())
    strXcoord = "X: "+ str(xCoord)
    movementXLabel = Label(movementFrame, text=strXcoord).grid(row=3, column=0, columnspan=2, sticky="ew")
    return xCoord

def lineeriXMove(xCoord):
    write_ser("G0 X-" + movementStepValue.get())
    xCoord = xCoord - float(movementStepValue.get())
    strXcoord = "X: " + str(xCoord)
    movementXLabel = Label(movementFrame, text=strXcoord).grid(row=3, column=0, columnspan=2, sticky="ew")
    return xCoord

def lineerYMove(yCoord):
    write_ser("G0 Y" + movementStepValue.get())
    yCoord = yCoord + float(movementStepValue.get())
    strYcoord = "Y: " + str(yCoord)
    movementYLabel = Label(movementFrame, text=strYcoord).grid(row=4, column=0, columnspan=2, sticky="ew")
    return yCoord

def lineeriYMove(yCoord):
    write_ser("G0 Y-" + movementStepValue.get())
    yCoord = yCoord - float(movementStepValue.get())
    strYcoord = "Y: " + str(yCoord)
    movementYLabel = Label(movementFrame, text=strYcoord).grid(row=4, column=0, columnspan=2, sticky="ew")
    return yCoord

def lineerZMove(zCoord):
    write_ser("G0 Z" + movementStepValue.get())
    zCoord = zCoord + float(movementStepValue.get())
    strZcoord = "Z: " + str(zCoord)
    movementYLabel = Label(movementFrame, text=strZcoord).grid(row=5, column=0, columnspan=2, sticky="ew")
    return zCoord

def lineeriZMove(zCoord):
    write_ser("G0 Z-" + movementStepValue.get())
    zCoord = zCoord - float(movementStepValue.get())
    strZcoord = "Z: " + str(zCoord)
    movementYLabel = Label(movementFrame, text=strZcoord).grid(row=5, column=0, columnspan=2, sticky="ew")
    return zCoord


yUpButton = Button(movementFrame, text="Y Up", command= lambda: lineerYMove(yCoord)).grid(row=0, column=1, sticky="ew")
yDownButton = Button(movementFrame, text="Y Down", command=lambda: lineeriYMove(yCoord)).grid(row=2, column=1, sticky="ew")
xRightButton = Button(movementFrame, text="X Right", command= lambda: lineerXMove(xCoord)).grid(row=1, column=2, sticky="ew")
xLeftButton = Button(movementFrame, text="X Left", command= lambda: lineeriXMove(xCoord)).grid(row=1, column=0, sticky="ew")
zUpButton = Button(movementFrame, text="Z Up", command= lambda: lineerZMove(zCoord)).grid(row=0, column=2, sticky="ew")
zDownButton = Button(movementFrame, text="Z Up", command= lambda: lineeriZMove(zCoord)).grid(row=2, column=2, sticky="ew")

emptyLabel2 = Label(movementFrame, text="").grid(row=0, column=0, sticky="ew")
emptyLabel2 = Label(movementFrame, text="").grid(row=2, column=0, sticky="ew")


### end - Frame - Lineer Movement



########################################################################################################



### Key Binds

root.bind('<Return>',lambda event:sendCommand())
root.bind('<Up>',lambda event:extrude())
root.bind('<Down>',lambda event:retract())

Grid.rowconfigure(root,0,weight=1)
Grid.columnconfigure(root,0,weight=1)

### end - Key Binds



########################################################################################################



### - Window - Calibrate

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


calibrateButton = Button(statusFrame, text="Calibrate", command=calibrateWindow).grid(row=1,column=0,columnspan=2,sticky="ew")


### end - Window - Calibrate



########################################################################################################



root.mainloop()
