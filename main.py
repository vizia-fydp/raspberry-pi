import time
import io
import cv2
import RPi.GPIO as GPIO
import numpy as np
from picamera import PiCamera
from enum import Enum


##########################
#       Constants        #
##########################
BUTTON1_PIN = 4
BUTTON2_PIN = 27
BUZZER_PIN = 5
BUZZER_FREQUENCY = 440 # Hz
BUTTON_BOUNCE_MS = 500
IMAGE_MAX_DIMENSION = 1000


#######################################
#          GLOBAL VARIABLES           #
#######################################
class Mode(Enum):
    TEXT = 0
    DOCUMENT = 1
    COLOR = 2
    MONEY = 3

mode = Mode.TEXT
camera = PiCamera()


#######################################
#       Buzzer helper functions       #
#######################################
def beep():
    buzzer.ChangeFrequency(BUZZER_FREQUENCY)
    buzzer.start(10) # duty cycle
    time.sleep(0.1)
    buzzer.stop()

def errorBeep():
    beep()
    time.sleep(0.1)
    beep()

def resizeImage(image):
    height, width, _ = image.shape
    scaled_height = 0
    scaled_width = 0

    if width > height:
        scaled_width = IMAGE_MAX_DIMENSION
        scaled_height = int(height / width * scaled_width)
    else:
        scaled_height = IMAGE_MAX_DIMENSION
        scaled_width = int(width / height * scaled_height)

    return cv2.resize(image, (scaled_width, scaled_height),
        interpolation = cv2.INTER_AREA)


#######################################
#      Interrupt Service Routines     #
#######################################
def button1(channel):
    # camera.capture("test.png")
    stream = io.BytesIO()
    camera.capture(stream, format="jpeg")

    # Construct a numpy array from the stream
    data = np.frombuffer(stream.getvalue(), dtype=np.uint8)

    # "Decode" the image from the array, preserving colour
    image = cv2.imdecode(data, 1)

    # Resize
    image = resizeImage(image)
    print(image.shape)

    cv2.imwrite("test.png", image)

    print("Button 1 pressed.")

def button2(channel):
    mode = (mode + 1) % len(Mode)
    print("Switched to mode {}".format(mode))


#######################################
#             GPIO Setup              #
#######################################

# Can use either pin numbers (BOARD) or Broadcom GPIO Numbers (BCM)
GPIO.setmode(GPIO.BCM)

# Setup buttons as inputs. GPIO.PUD_DOWN means use internal pull down resister.
# Button is HIGH while pressed, and LOW while not pressed
GPIO.setup(BUTTON1_PIN, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(BUTTON2_PIN, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

# Setup buzzer
GPIO.setup(BUZZER_PIN, GPIO.OUT)
buzzer = GPIO.PWM(BUZZER_PIN, BUZZER_FREQUENCY)

# Setup interrupts on falling edge (button released)
GPIO.add_event_detect(BUTTON1_PIN, GPIO.FALLING, callback = button1,
    bouncetime = BUTTON_BOUNCE_MS)
GPIO.add_event_detect(BUTTON2_PIN, GPIO.FALLING, callback = button2,
    bouncetime = BUTTON_BOUNCE_MS)


#######################################
#     Loop to keep program running    #
#######################################
try:
    while True:
        time.sleep(1)
except:
    GPIO.cleanup()
