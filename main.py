import base64
import time
import io
import json
import cv2
import requests
import RPi.GPIO as GPIO
import numpy as np
from picamera import PiCamera
from enum import Enum


##########################
#       Constants        #
##########################

SERVER_URL = "https://7852-64-229-183-215.ngrok.io"

# Pins
BUTTON1_PIN = 4
BUTTON2_PIN = 27
BUZZER_PIN = 5

# SocketIO paths that iOS app listens on
IOS_INFO = "iOS_info"
IOS_RESULTS = "iOS_results"

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
#           Helper functions          #
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
#              API Calls              #
#######################################

def socket_emit(path, msg):
    params = {"path": path}
    response = requests.post(
        url = "{}/socket_emit".format(SERVER_URL),
        data = msg,
        params = params
    )
    if response.status_code != 200:
        errorBeep()

def ocr(img, type):
    # Prepare headers and params for http request
    headers = {"content-type": "image/jpeg"}
    params = {"type": type, "socket_emit_path": IOS_RESULTS}

    # Encode image as jpeg and convert to base64 string
    _, img_arr = cv2.imencode('.jpg', img)
    img_encoded = base64.b64encode(img_arr.tobytes())

    # Send request
    response = requests.post(
        url = "{}/ocr".format(SERVER_URL),
        data = img_encoded,
        headers = headers,
        params = params
    )

    if response.status_code != 200:
        print("ocr error")
        errorBeep()
    else:
        print(json.loads(response.text))

def detect_color(img):
    # Prepare headers and params for http request
    headers = {"content-type": "image/jpeg"}
    params = {"k": 3, "socket_emit_path": IOS_RESULTS}

    # Encode image as jpeg
    _, img_encoded = cv2.imencode(".jpg", img)

    # Send request
    response = requests.post(
        url = "{}/detect_color".format(SERVER_URL),
        data = img_encoded.tobytes(),
        headers = headers,
        params = params
    )

    if response.status_code != 200:
        print("detect_color error")
        errorBeep()
    else:
        print(json.loads(response.text))

def classify_money(img):
    # Prepare headers and params for http request
    headers = {"content-type": "image/jpeg"}
    params = {"socket_emit_path": IOS_RESULTS}

    # Encode image as jpeg
    _, img_encoded = cv2.imencode(".jpg", img)

    # Send request
    response = requests.post(
        url = "{}/classify_money".format(SERVER_URL),
        data = img_encoded.tobytes(),
        headers = headers,
        params = params
    )

    if response.status_code != 200:
        print("classify_money error")
        errorBeep()
    else:
        print(json.loads(response.text))


#######################################
#      Interrupt Service Routines     #
#######################################
def button1(channel):
    # Capture image from picam
    stream = io.BytesIO()
    camera.capture(stream, format="jpeg")

    # Construct a numpy array from the stream
    data = np.frombuffer(stream.getvalue(), dtype=np.uint8)

    # "Decode" the image from the array, preserving colour
    image = cv2.imdecode(data, 1)

    # Resize
    image = resizeImage(image)

    # Make API call based on which mode we are in
    if mode == Mode.TEXT:
        ocr(image, "TEXT_DETECTION")
    elif mode == Mode.DOCUMENT:
        ocr(image, "DOCUMENT_TEXT_DETECTION")
    elif mode == Mode.COLOR:
        detect_color(image)
    elif mode == Mode.MONEY:
        classify_money(image)

def button2(channel):
    global mode
    mode = Mode((mode.value + 1) % len(Mode))

    # Emit on IOS_INFO socket so app can announce mode switch
    socket_emit(IOS_INFO, str(mode.name))
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
