import serial
import time


def checkConnection(portNum):

    MAX_BUFF_LEN = 255
    SETUP = False
    port = None
    stat = ""
    prev = time.time()

    if (not SETUP):

        try:

            port = serial.Serial(portNum, 115200, timeout=1) #COM3 is my connection port of the printer

        except:  # Bad way of writing excepts (always know your errors)
            stat = "Not Conneted!"
            if (time.time() - prev > 2):  # Don't spam with msg
                stat = "No Connetiion!"
                prev = time.time()

        if (port is not None):  # We're connected
            SETUP = True
            stat = "Conneted!"

    return stat,port




