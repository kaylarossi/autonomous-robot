#
# kmr262 3/20/22 two_wheel.py
#
# function to drive motors full speed, CCW, and CW includ stop motor
#   parameters: servo number, direction (CW, CCW, stop)
#
# control servos using physical buttons with functions:
#   left servo, CW          left servo stop         left servo CCW
#   right servo, CW         right servo stop        right servo CCW
#
# servo direction reference: 
# CCW IN1 L IN2 H           CW IN1H IN2L            stop IN1L IN2L

import RPi.GPIO as GPIO
import time
import subprocess
import os
GPIO.setwarnings(False)

# set up GPIO pins
GPIO.setmode(GPIO.BCM)
# PWM 
GPIO.setup(13, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)
#initialize PWM at 50 Hz for both channels
p1 = GPIO.PWM(13, 50)
dc1 = (0)
p1.start(dc1)

p2 = GPIO.PWM(19, 50)
dc2 = (0)
p2.start(dc2)

# set up input for buttons on piTFT and additional buttons
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)# second TFT button
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)# button TFT button
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)# top TFT button
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)# third TFT button
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def drive(num, d):
    # parameters - servo number (num) and direction (d) 
    # allowed variables for servo number: 1, 2
    # allowed variables for direction: CW, CCW, stop
    if num == 1:
        #init motor 1 B channel
        # IN1(6) IN2(5)
        GPIO.setup(5, GPIO.OUT)
        GPIO.setup(6, GPIO.OUT)
        if (d == str('CW')):
            # motor 1 B channel CW
            GPIO.output(6, GPIO.HIGH)
            GPIO.output(5, GPIO.LOW)
            p1.ChangeDutyCycle(100)

        if (d == str('CCW')):
            # motor 1 B channel CCW
            GPIO.output(6, GPIO.LOW)
            GPIO.output(5, GPIO.HIGH)
            p1.ChangeDutyCycle(100)

        if (d == str('stop')):
            GPIO.output(6, GPIO.LOW)
            GPIO.output(5, GPIO.LOW)
            p1.ChangeDutyCycle(0)

            
    if num == 2:
        #init motor 2 A channel
        # IN1(24) IN2(16)
        GPIO.setup(24, GPIO.OUT)
        GPIO.setup(16, GPIO.OUT)
        if (d == str('CW')):
            # motor 2 A channel CW
            GPIO.output(24, GPIO.HIGH)
            GPIO.output(16, GPIO.LOW)
            p2.ChangeDutyCycle(100)
        if (d == str('CCW')):
            #motor 2 A channel CCW
            GPIO.output(24, GPIO.LOW)
            GPIO.output(16, GPIO.HIGH)
            p2.ChangeDutyCycle(100)
        if (d == str('stop')):
            GPIO.output(24, GPIO.LOW)
            GPIO.output(16, GPIO.LOW)
            p2.ChangeDutyCycle(0)
  
#callback setup
def GPIO17_cb(channel):
    print('motor 1, clockwise')
    cmd17 = drive(1, 'CW')

def GPIO22_cb(channel):
    print('motor 1, stopped')
    cmd22 = drive(1, 'stop')

def GPIO23_cb(channel):
    print('motor 1, counter-clockwise')
    cmd23 = drive(1, 'CCW')

def GPIO27_cb(channel):
    print('motor 2, clockwise')
    cmd27 = drive(2, 'CW')

def GPIO12_cb(channel):
    print('motor 2, stopped')
    cmd12 = drive(2, 'stop')

def GPIO26_cb(channel):
    print('motor 2, counter-clockwise')
    cmd26 = drive(2, 'CCW')

#connect callback routine to GPIO
GPIO.add_event_detect(17, GPIO.FALLING, callback=GPIO17_cb, bouncetime=300)
GPIO.add_event_detect(22, GPIO.FALLING, callback=GPIO22_cb, bouncetime=300)
GPIO.add_event_detect(23, GPIO.FALLING, callback=GPIO23_cb, bouncetime=300)
GPIO.add_event_detect(27, GPIO.FALLING, callback=GPIO27_cb, bouncetime=300)
GPIO.add_event_detect(12, GPIO.FALLING, callback=GPIO12_cb, bouncetime=300)
GPIO.add_event_detect(26, GPIO.FALLING, callback=GPIO26_cb, bouncetime=300)


starttime = time.time()
timeout = 40
code_run = True
while code_run:
    time.sleep(0.2)
# time code quit
    now = time.time()
    elaptime = now - starttime
    if elaptime > timeout:
        print('end')
        code_run = False


GPIO.cleanup()
