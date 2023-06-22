import RPi.GPIO as GPIO
import math
import os
from datetime import datetime
from time import sleep

############
# CONSTANTS#
############

### IR VALUES
# # Input pin is 15 (GPIO22)
# INPUT_PIN = 15
# Input pin is 7 (GPIO4)
INPUT_PIN = 7


# To turn on debug print outs, set to 1
DEBUG = 0

############
# VARIABLES#
############

############
# FUNCTIONS#
############

# This function receives a numeric code and returns the associated key
def irLUT(dataCode):
    key = ""
    isNum = ""

    # NUMERICAL KEYS
    if(dataCode == 0x68):
        key = "1"
        isNum = 1
    if(dataCode == 0x98):
        key = "2"
        isNum = 1
    if(dataCode == 0xB0):
        key = "3"
        isNum = 1
    if(dataCode == 0x30):
        key = "4"
        isNum = 1
    if(dataCode == 0x18):
        key = "5"
        isNum = 1
    if(dataCode == 0x7A):
        key = "6"
        isNum = 1
    if(dataCode == 0x00):
        key = "7"
        isNum = 1
    if(dataCode == 0x38):
        key = "8"
        isNum = 1
    if(dataCode == 0x00):
        key = "9"
        isNum = 1
    if(dataCode == 0x4A):
        key = "0"
        isNum = 1

    # NON_NUMERICAL KEYS
    if(dataCode == 0x52):
        key = "#"
        isNum = 0
    if(dataCode == 0x42):
        key = "*"
        isNum = 0
    if(dataCode == 0x10):
        key = "LEFT_KEY"
        isNum = 0
    if(dataCode == 0x5A):
        key = "RIGHT_KEY"
        isNum = 0
    if(dataCode == 0x62):
        key = "UP_KEY"
        isNum = 0
    if(dataCode == 0xA8):
        key = "DOWN_KEY"
        isNum = 0
    if(dataCode == 0x02):
        key = "OK_KEY"
        isNum = 0

    return key, isNum

# This function receives arrays of pulses and their durations, and
# it attempts to decode a packet using the NEC protocol
def decodeIR(pulseValues, timeValues):
    #################
    # Start decoding#
    #################
    if(DEBUG==1):
        print("Size of array is {}".format(len(pulseValues)))
        print(pulseValues)
        print(timeValues)

    commandList = []
    # build a new list for individually decoded bits
    for t in range(5, len(timeValues), 2):
        # use time threshold to distinguish between long and short pulses of 0
        if (DEBUG==1):
            print("Duration of {}th zero: {}".format(t, timeValues[t]))
        if (timeValues[t] < 1000):
            commandList.append("0")
        else:
            commandList.append("1")

    commandNum = int("".join(str(x) for x in commandList), 2)
    if(DEBUG==1):
        print("Command: 0b{:032b}".format(commandNum))
        print("Command: 0x{:08x}".format(commandNum))

    #################
    # Error checking#
    #################

    # Look at low/high bytes for address/data fields
    addressHigh = (commandNum & 0xFF000000) >> 24
    addressLow = (commandNum & 0x00FF0000) >> 16
    dataHigh = (commandNum & 0x0000FF00) >> 8
    dataLow = (commandNum & 0x000000FF)
    if (DEBUG==1): 
        print("Address byte high:\t 0x{:02x}".format(addressHigh))
        print("Address byte low:\t 0x{:02x}".format(addressLow))
        print("Data byte low:\t\t 0x{:02x}".format(dataLow))

    # Print key code
    print("Data byte high:\t\t 0x{:02x}".format(dataHigh))
    

    # Error checking according to original NEC protocol
    if(addressHigh+addressLow != 0xFF):
        print("Address bytes do not match!")
        return [-1,-1]
    if(dataHigh+dataLow != 0xFF):
        print("Data bytes do not match!")
        return [-1,-1]

    key, isNum = irLUT(dataHigh)
    
    return key, isNum

###################
# INITIALIZE PINS #
###################
GPIO.setwarnings(False) 
GPIO.setmode(GPIO.BOARD)
GPIO.setup(INPUT_PIN, GPIO.IN)

# Main loop, listen for infinite packets
while True:
    print("\nListening for an IR packet")

    # If there was a transmission, wait until it finishes
    value = 1
    while value:
        value = GPIO.input(INPUT_PIN)

    # timestamps for pulses and packet reception
    startTimePulse = datetime.now()
    previousPacketTime = 0

    # Buffers the pulse value and time durations
    pulseValues = []
    timeValues = []

    # Variable used to keep track of state transitions
    previousVal = 0

    # Inner loop 
    while True:
        # Measure time up state change
        if value != previousVal:
            # The value has changed, so calculate the length of this run
            now = datetime.now()
            pulseLength = now - startTimePulse
            startTimePulse = now

            # Record value and duration of current state
            pulseValues.append(value)
            timeValues.append(pulseLength.microseconds)
            
            # Detect short IR packet using packet length and special timing
            if(len(pulseValues) == 3):
                if(timeValues[1] < 3000):
                    print("Detected Short IR packet")
                    if(DEBUG==1):
                        print(pulseValues)
                        print(timeValues)
                    break

            # Detect standard IR packet using packet length 
            if(len(pulseValues) == 67):
                print("Finished receiving IR packet")
                [key, isNum] = decodeIR(pulseValues, timeValues)

                if (key != -1):
                    # To Do: Assignment 6
                    print("Key {} has been pressed".format(key))

                    if(key == "LEFT_KEY"):
                        f = open("/var/www/html/light", "w")
                        f.write("1")
                        f.close()
                    
                    if(key == "RIGHT_KEY"):
                        f = open("/var/www/html/light", "w")
                        f.write("0")
                        f.close()

                    # if(key == "LEFT_KEY"):
                    #     wheelNum = max(wheelNum-25,0)
                    #     setColor(wheelNum)
                    #
                    # if(key == "RIGHT_KEY"):
                    #     wheelNum = min(wheelNum+25,255)
                    #     setColor(wheelNum)
                    #
                    # if(key == "UP_KEY"):
                    #     brightness = min(brightness+25,255)
                    #     setBrightness(brightness)
                    #
                    # if(key == "DOWN_KEY"):
                    #     brightness = max(brightness-25,0)
                    #     setBrightness(brightness)

                break

        # save state
        previousVal = value
        # read GPIO pin
        value = GPIO.input(INPUT_PIN)
