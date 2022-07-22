#
# kmr262 3/16/22 blink with pwm
#
# set freq 1 Hz with duty cycle 50%
# include integer arg. used to adjust blink freq

import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(13, GPIO.OUT)

#prompt  = "Enter blink frequency: "

blinkfreq = 10

#start blinking at 1 Hz
p = GPIO.PWM(13, 1)
# 50% duty cycle
p.start(50)

blinking = True
while blinking:
    prompt = "Enter blink frequency: "
    blinkfreq = int(input(prompt))
    if blinkfreq == 0:
        blinking = False
    else:
#change blink frequency
        p.ChangeFrequency(blinkfreq)

GPIO.cleanup()
