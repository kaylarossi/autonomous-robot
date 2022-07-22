#
# kmr262 3/16/22 
#
# blink LED without using PWM
#
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
#set GPIO 13 as output to blink LED
GPIO.setup(13, GPIO.OUT)

i = 0
while (i<10):
    GPIO.output(13, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(13, GPIO.LOW)
    time.sleep(0.5)
    i = i + 1

GPIO.cleanup()
