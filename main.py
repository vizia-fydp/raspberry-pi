# https://roboticsbackend.com/raspberry-pi-gpio-interrupts-tutorial/
import RPi.GPIO as GPIO
import time

######### Constants #########
BUTTON1_PIN = 4
BUTTON2_PIN = 27
BUZZER_PIN = 5
BUTTON_BOUNCE_MS = 50

######### Interrupt service routines #########
def button1(channel):
    print("Button 1 pressed.")
def button2(channel):
    print("Button 2 pressed.")

######### GPIO Setup #########

# Can use either pin numbers (BOARD) or Broadcom GPIO Numbers (BCM)
GPIO.setmode(GPIO.BCM)

# Setup buttons as inputs. GPIO.PUD_UP means use internal pull up resister.
# Button is HIGH while not pressed, and LOW while pressed
GPIO.setup(BUTTON1_PIN, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(BUTTON2_PIN, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

# Setup interrupts on rising edge (button released)
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
