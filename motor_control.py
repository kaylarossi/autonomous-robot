#
# kmr262 3/16/22 motor_control.py
#
# when program starts, motor is stopped
# speed ranges through 3 speeds - stopped, half, full in CW
# each speed increment for 3 seconds and print when changing speed
# return to stopped state

import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)

# set up GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(19, GPIO.OUT)    #LED PWM monitoring
GPIO.setup(16, GPIO.OUT)     #motor control
GPIO.setup(24, GPIO.OUT)     #motor control

#initialize PWM at 50 Hz
p = GPIO.PWM(19, 50) #13
dc = 0
p.start(dc)

#initialize motor 1 input high/low - stopped upon program start
# CW: IN1(6)24 = H , IN2(5)25 = L
# CCW: IN1 = L , IN2 = H
GPIO.output(24, GPIO.LOW)
GPIO.output(16, GPIO.LOW)

# motor stopped when start for 3 seconds
print('motor stopped')
time.sleep(3)

# settings for CW direction
GPIO.output(24, GPIO.HIGH)
GPIO.output(16, GPIO.LOW)

# half speed CW direction for 3 seconds
print('motor running at half speed CW')
p.ChangeDutyCycle(50)
time.sleep(3)
 
# full speed CW direction for 3 seconds
print('motor running at full speed CW')
p.ChangeDutyCycle(100)
time.sleep(3)

# stop motor settings
GPIO.output(16, GPIO.LOW)
GPIO.output(24, GPIO.LOW)
print('motor stopped')
time.sleep(3)

# settings for CCW direction
GPIO.output(24, GPIO.LOW)
GPIO.output(16, GPIO.HIGH)

# half speed CCW direction 3 seconds
print('motor running at half speed CCW')
p.ChangeDutyCycle(50)
time.sleep(3)

# full speed CCW direction for 3 seconds
print('motor running at full speed CCW')
p.ChangeDutyCycle(100)
time.sleep(3)

#servo return to stopped
print('end')
p.ChangeDutyCycle(0)
p.stop()
time.sleep(1)

GPIO.cleanup()

