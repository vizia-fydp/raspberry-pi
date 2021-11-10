
#
# REVISION HISTORY
#
# 21/08/01 - zdenno, created

#
# IMPORTS
#
from time import sleep
from picamera import PiCamera

camera = PiCamera()
camera.resolution = (1024,768)
camera.start_preview()

sleep(2)
camera.capture('test.jpg')

