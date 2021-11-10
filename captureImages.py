#######################################
#              IMPORTS                #
#######################################
import RPi.GPIO as gpio
import os
import shutil

from picamera import PiCamera
from time import sleep

#######################################
#          GLOBAL VARIABLES           #
#######################################
imageDir = os.path.join(os.getcwd(), "images")
camera = PiCamera()

#######################################
#             CALLBACK                #
#######################################
def captureAndWrite(self):
    if len(os.listdir(imageDir)) == 0:
        newImagePath = os.path.join(imageDir, "0.jpg")
    else:
        imageCtr = max(list(filter(lambda x: int(x.replace(".jpg", "")), os.listdir(imageDir))))
        newImagePath = os.path.join(imageDir, "{}.jpg".format(imageCtr+1))
    camera.capture(newImagePath)
    print("Captured {}\r\n".format(newImagePath))

#######################################
#            MAIN SCRIPT              #
#######################################

# Initialize Pin
gpio.setwarnings(False)
gpio.setmode(gpio.BOARD)
gpio.setup(7, gpio.IN, pull_up_down=gpio.PUD_DOWN)

# Check for image folder
if not (os.path.isdir(imageDir)):
    os.makedirs(imageDir)
else:
    shutil.rmtree(imageDir)
    os.makedirs(imageDir)

# Setup Camera
camera.resolution = (3280,2464)
camera.start_preview()

# Connect Event and Callback
gpio.add_event_detect(7, gpio.RISING, callback=captureAndWrite)

message = input("Press enter when done\r\n")

gpio.cleanup()

