import RPi.GPIO as GPIO
import time
from picamera import PiCamera


##########################
#       Constants        #
##########################
BUTTON1_PIN = 4
BUTTON2_PIN = 27
BUZZER_PIN = 5
BUZZER_FREQUENCY = 440 # Hz
BUTTON_BOUNCE_MS = 500


#######################################
#          GLOBAL VARIABLES           #
#######################################
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


#######################################
#      Interrupt Service Routines     #
#######################################
def button1(channel):
    camera.capture("test.png")
    print("Button 1 pressed.")

def button2(channel):
    errorBeep()
    print("Button 2 pressed.")


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
