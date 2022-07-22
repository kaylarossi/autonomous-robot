#
# kmr262 test_run.py 3/27/22
#
# piTFT screen display:
#   direction for each motor (CW, CCW, stopped) R or L
#   red 'stop' button - when pressed motors immediately stop,
#                       changes to green 'resume' button
#   'quit' button - when pressed ends program and returns to CML in linux
#   'start' button - run program
#   record start-time/direction pairs for each motor and display scrolling
#   history of recent motion (3 past entries included)


import RPi.GPIO as GPIO
import time
import os
import pygame
from pygame.locals import*

os.putenv('SDL_VIDEODRIVER', 'fbcon') #Display on piTFT
os.putenv('SDL_FBDEV', '/dev/fb0')  #
os.putenv('SDL_MOUSEDRV', 'TSLIB') #track mouse clicks on piTFT
os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')

pygame.init()
#pygame.mouse.set_visible(False)
screen = pygame.display.set_mode((320,240))
white = [255, 255, 255]
black = [0, 0, 0]
red = [255, 0, 0]
green = [0, 255, 0]
my_font = pygame.font.Font(None, 25)

###### GPIO SET UP AND INIT######

#GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

#PWM set up
GPIO.setup(13, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)
#initialize PWM at 50 Hz for both channels
p1 = GPIO.PWM(13, 50)
p1.start(0)

p2 = GPIO.PWM(19, 50)
p2.start(0)

# set up input for buttons on piTFT and additional buttons
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)

##### FUNCTIONS #####
GPIO.setup(5, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)
GPIO.setup(12, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)

# drive function for motor control:
def drive(num, d):
    print(str(num), d)
    # parameters - servo number (num) and direction (d)
    # allowed variables for servo number: 1, 2
    # allowed variables for direction: CW, CCW, stop
    if num == 1:
        #init motor 1 B channel - RED ORANGE LEADS
        # IN1(6) IN2(5)
        # LEFT MOTOR
        if (d == str('CCW')):
            # motor 1 B channel CW
            GPIO.output(6, GPIO.HIGH)
            GPIO.output(5, GPIO.LOW)
            p1.ChangeDutyCycle(50)
            if llog[0] != str('CCW'):
                llog.insert(0, 'CCW')
                llog.pop(3)
                lintime.insert(0, int(elaptime))
                lintime.pop(3)

        if (d == str('CW')):
            # motor 1 B channel CCW
            GPIO.output(6, GPIO.LOW)
            GPIO.output(5, GPIO.HIGH)
            p1.ChangeDutyCycle(50)
            if llog[0] != str('CW'):
                llog.insert(0,'CW')
                llog.pop(3)
                lintime.insert(0, int(elaptime))
                lintime.pop(3)

        if (d == str('stop')):
            GPIO.output(6, GPIO.LOW)
            GPIO.output(5, GPIO.LOW)
            p1.ChangeDutyCycle(0)
            if llog[0] != str('Stop'):
                llog.insert(0, 'Stop')
                llog.pop(3)
                lintime.insert(0, int(elaptime))
                lintime.pop(3)

    if num == 2:
        #init motor 2 A channel - BLUE GREEN LEADS
        # IN1(24) IN2(16)
        # RIGHT MOTOR
        if (d == str('CW')):
            # motor 2 A channel CW
            GPIO.output(12, GPIO.HIGH)
            GPIO.output(16, GPIO.LOW)
            p2.ChangeDutyCycle(50)
            if rlog[0] != str('CW'):
                rlog.insert(0,'CW')
                rlog.pop(3)
                rintime.insert(0, int(elaptime))
                rintime.pop(3)
        if (d == str('CCW')):
            #motor 2 A channel CCW
            GPIO.output(12, GPIO.LOW)
            GPIO.output(16, GPIO.HIGH)
            p2.ChangeDutyCycle(50)
            if rlog[0] != str('CCW'):
                rlog.insert(0,'CCW')
                rlog.pop(3)
                rintime.insert(0, int(elaptime))
                rintime.pop(3)
        if (d == str('stop')):
            GPIO.output(12, GPIO.LOW)
            GPIO.output(16, GPIO.LOW)
            p2.ChangeDutyCycle(0)
            if rlog[0] != str('Stop'):
                rlog.insert(0, 'Stop')
                rlog.pop(3)
                rintime.insert(0, int(elaptime))
                rintime.pop(3)

#callback setup for phyiscal quit

def GPIO27_cb(channel):
    print('Physical quit pressed')
    button_run = False

#connect callback routine to GPIO
GPIO.add_event_detect(27, GPIO.FALLING, callback=GPIO27_cb, bouncetime=300)

###### PYGAME AND SCREEN INIT ######

def stop():
    # circle is resume and turns green, motors are paused
    drive(1, 'stop')
    drive(2, 'stop')
    stoptime = elaptime

def resume():
    # circle is stop, turns red, motors resume
    drive(1, llog[1])
    drive(2, rlog[1])
    newetime = stoptime
    #timestart = timenow
    #timenow = timenow + stoptime
    
def drawcircle(chcolor):
    if chcolor == 1:
        color = red
    if chcolor == 2:
        color = green
    pygame.draw.circle(screen, color, [160, 120], 45, 0)

def forward():
    drive(1, 'CCW')
    drive(2, 'CCW')

def backward():
    drive(1, 'CW')
    drive(2, 'CW')

def sequence(tog, time):
   # print('seq ' + str(time))
    if tog:
        if (time % modval < 3):
            forward()
        elif (time % modval < 6):
            stop()
        elif (time % modval < 9):
            backward()
        elif (time % modval < 12):
            drive(2, 'CCW')
            drive(1, 'stop')
        elif (time % modval  < 15):
            stop()
        elif (time % modval < 18):
            drive(1, 'CCW')  
            drive(2, 'stop')
        elif (time % modval < 21):
            stop()

# Lists
lintime = [0,0,0]
rintime = [0,0,0]
llog = ['Stop', 'Stop', 'Stop']
rlog = ['Stop', 'Stop', 'Stop']
# Dictionaries
running_b = {'start':(90,200),'quit':(220,200),'Left History':(60, 30), 'Right History':(260, 30), 'STOP':(160, 120)}
left_log = {0:(30,80), 1:(30, 110), 2: (30, 140)}
left_time = {0:(100, 80), 1:(100,110), 2:(100, 140)}
right_log= {0:(230,80), 1:(230,110), 2: (230,140)}
right_time = {0: (290, 80), 1: (290, 110), 2: (290, 140)}

screen.fill(white)  #erase workspace
button_run = True
timeout = 500
starttime = time.time()
chcolor = 1
modval = 21
tog = False
newetime = 0
stoptime = 0


while button_run:
    time.sleep(0.2)
    screen.fill(white)

    now = time.time()
    elaptime = now-starttime

    # time bail
    if elaptime > timeout:
        button_run = False

    #Display STOP and quit buttons and lists 
    drawcircle(chcolor)

    running_b_rect = {}
    for my_text, text_pos in running_b.items():
        text_surface = my_font.render(my_text, True, black)
        rect = text_surface.get_rect(center=text_pos)
        screen.blit(text_surface, rect)
        running_b_rect[my_text] = rect # rect for text button

    for l_text, l_pos in left_log.items():
        l_surface = my_font.render(llog[l_text], True, black)
        l_rect = l_surface.get_rect(center=l_pos)
        screen.blit(l_surface, l_rect)
    for r_text, r_pos in right_log.items():
        r_surface = my_font.render(rlog[r_text], True, black)
        r_rect = r_surface.get_rect(center=r_pos)
        screen.blit(r_surface, r_rect)
    for lf_text, lf_pos in left_time.items():
        lf_surface = my_font.render(str(lintime[lf_text]), True, black)
        lf_rect = lf_surface.get_rect(center=lf_pos)
        screen.blit(lf_surface, lf_rect)
    for rt_text, rt_pos in right_time.items():
        rt_surface = my_font.render(str(rintime[rt_text]), True, black)
        rt_rect = rt_surface.get_rect(center=rt_pos)
        screen.blit(rt_surface, rt_rect)


    pygame.display.flip()
 
    sequence(tog, elaptime-newetime)

    # look for touch 
    for event in pygame.event.get():
        if(event.type is MOUSEBUTTONDOWN):
            pos=pygame.mouse.get_pos()
        elif(event.type is MOUSEBUTTONUP):
            pos = pygame.mouse.get_pos()
            x,y = pos
            print(pos)
            for (my_text, rect) in running_b_rect.items():
                if(rect.collidepoint(pos)):
                    if (my_text == str('start')):
                        print('start pressed')
                        print('e ' + str(elaptime))
                        #start sequence
                        tog = True
                        newetime = elaptime
                        print('n '+ str(newetime))
                        
                    if (my_text == str('quit')):
                        print('quit pressed')
                        button_run = False
                    
                    if (my_text == str('STOP')):
                        print('stop pressed')
                        tog = False
                        stop()
                        running_b['RESUME'] = running_b.pop('STOP')
                        chcolor = 2
                        
                    if (my_text == str('RESUME')):
                        print('resume pressed')
                        tog = True
                        resume()
                        running_b['STOP'] = running_b.pop('RESUME')
                        chcolor = 1

                        


time.sleep(1)
GPIO.cleanup()

