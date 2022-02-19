# https://roboticsbackend.com/raspberry-pi-gpio-interrupts-tutorial/
import RPi.GPIO as GPIO
from gpiozero import TonalBuzzer
from gpiozero.tones import Tone
import time

######### Constants #########
BUTTON1_PIN = 4
BUTTON2_PIN = 27
BUZZER_PIN = 5
BUTTON_BOUNCE_MS = 50

def beep():
    buzzer.start(50)
    time.sleep(1)
    buzzer.stop()

######### Interrupt service routines #########
def button1(channel):
    beep()
    print("Button 1 pressed.")

def button2(channel):
    print("Button 2 pressed.")

######### GPIO Setup #########

# Can use either pin numbers (BOARD) or Broadcom GPIO Numbers (BCM)
GPIO.setmode(GPIO.BCM)

# Setup buttons as inputs. GPIO.PUD_DOWN means use internal pull down resister.
# Button is HIGH while pressed, and LOW while not pressed
GPIO.setup(BUTTON1_PIN, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(BUTTON2_PIN, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

# Setup buzzer as an output
GPIO.setup(BUZZER_PIN, GPIO.OUT)
global buzzer
buzzer = GPIO.PWM(BUZZER_PIN, 440)

# Setup interrupts on falling edge (button released)
GPIO.add_event_detect(BUTTON1_PIN, GPIO.FALLING, callback = button1,
    bouncetime = BUTTON_BOUNCE_MS)
GPIO.add_event_detect(BUTTON2_PIN, GPIO.FALLING, callback = button2,
    bouncetime = BUTTON_BOUNCE_MS)

######### Event loop to keep the program running #########
try:
    while True:
        time.sleep(1)
except:
    GPIO.cleanup()
