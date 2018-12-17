import RPi.GPIO as GPIO
from time import sleep

# https://pinout.xyz/
# pin 11 - flipper Left
# pin 12 - flipper Right
global pin_Flipper_Left
global pin_Flipper_Right
global flag_Flipper_Left
global flag_Flipper_Right
pin_Flipper_Left = 11
pin_Flipper_Right = 12
flag_Flipper_Left = False
flag_Flipper_Right = False

# pin 37 - Launch button
global pin_Button_Launch
global flag_Button_Launch
pin_Button_Launch = 37
flag_Button_Launch = False

# pin 29 - Left (X)
global pin_Button_X
pin_Button_X = 29
global flag_Button_X
flag_Button_X = False
# pin 31 - Down (A)
global pin_Button_A
pin_Button_A = 31
global flag_Button_A
flag_Button_A = False
# pin 32 - Up (Y)
global pin_Button_Y
pin_Button_Y = 32
global flag_Button_Y
flag_Button_Y = False
# pin 33 - Right (B)
global pin_Button_B
pin_Button_B = 33
global flag_Button_B
flag_Button_B = False

# pin 15 and 16 - Plunger
global pin_Plunger_Trigger
pin_Plunger_Trigger = 15
global pin_Plunger_Echo
pin_Plunger_Echo = 16
# last 3 distances measured, to apply low pass filter across the 3
global distance_prevT0 
distance_prevT0 = 0
global distance_prevT1
distance_prevT1 = 0
global distance_prevT2
distance_prevT2 = 0
# most recent plunger distance
global plunger_distance
plunger_distance = 0
# the distance needs to change by at least this value to report it
global plunger_threshold 
plunger_threshold = 5


def init_GPIO():   
    return


def init_flipper_buttons():
    # add an interrupt on pin number 7 on rising edge
    GPIO.add_event_detect(pin_Flipper_Left, GPIO.RISING, callback=button_pressed, bouncetime=300)
    GPIO.add_event_detect(pin_Flipper_Right, GPIO.RISING, callback=button_pressed, bouncetime=300)
    
    GPIO.add_event_detect(pin_Button_Launch, GPIO.RISING, callback=button_pressed, bouncetime=300)

    GPIO.add_event_detect(pin_Button_A, GPIO.RISING, callback=button_pressed, bouncetime=300)
    GPIO.add_event_detect(pin_Button_B, GPIO.RISING, callback=button_pressed, bouncetime=300)
    GPIO.add_event_detect(pin_Button_X, GPIO.RISING, callback=button_pressed, bouncetime=300)
    GPIO.add_event_detect(pin_Button_Y, GPIO.RISING, callback=button_pressed, bouncetime=300)


def init():
    # make all your initialization here
    init_GPIO()
    init_flipper_buttons()


    # callback = function which call when a signal rising edge on pin 
def button_pressed(channel):
    #import globals
    global flag_Flipper_Left
    global flag_Flipper_Right
    global flag_Button_Launch
    global flag_Button_A
    global flag_Button_B
    global flag_Button_X
    global flag_Button_Y

    #flippers
    if channel == pin_Flipper_Left:
        flag_Flipper_Left = True
        return
    if channel == pin_Flipper_Right:
        flag_Flipper_Right = True
        return

    # launch button
    if channel == pin_Button_Launch:
        flag_Button_Launch = True
        return
        
    # XBox buttons
    if channel == pin_Button_A:
        flag_Button_A = True
        return
    if channel == pin_Button_B:
        flag_Button_B = True
        return
    if channel == pin_Button_X:
        flag_Button_X = True
        return
    if channel == pin_Button_Y:
        flag_Button_Y = True
        return


def measure_plunger():
    # import globals
    global distance_prevT0
    global distance_prevT1
    global distance_prevT2
    global plunger_distance
    
    # previous smoothed measurements
    previousAvg = get_average_distance()
    
    # rotate the raw measurements
    distance_prevT2 = distance_prevT1
    distance_prevT1 = distance_prevT0
    distance_prevT0 = get_ultrasonic_distance()
    
    # current smoothed measurement
    newAvg = get_average_distance()

    if previousAvg == 0:        
        plunger_distance = newAvg # just report the new value if we were at 0
        return True

    # is the change big enough to report?    
    elif abs(newAvg / previousAvg) >= plunger_threshold:
        plunger_distance = newAvg
        return True

    return False


def get_average_distance():
    #import globals
    global distance_prevT0
    global distance_prevT1
    global distance_prevT2

    return (distance_prevT0 + distance_prevT1 + distance_prevT2) / 3


def get_ultrasonic_distance():
    #import globals
    global pin_Plunger_Trigger
    global pin_Plunger_Echo

    # set Trigger to HIGH
    GPIO.output(pin_Plunger_Trigger, True)
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(pin_Plunger_Trigger, False)
    StartTime = time.time_ns()
    StopTime = time.time_ns()
 
    # save StartTime until the ECHO pin is high;
    # the echo pin will go high when the trigger is sent
    while GPIO.input(pin_Plunger_Echo) == 0:
        StartTime = time.time_ns()
 
    # save time of arrival until the ECHO pin is low;
    # the echo pin will go low when the echo is received
    while GPIO.input(pin_Plunger_Echo) == 1:
        StopTime = time.time_ns()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance



global NULL_CHAR
NULL_CHAR = chr(0)
def write_report(report):
    with open('/dev/hidg0', 'rb+') as fd:
        fd.write(report.encode())

def report(pin):
    global flag_Flipper_Left
    global flag_Flipper_Right
    global flag_Button_A
    global flag_Button_B
    global flag_Button_X
    global flag_Button_Y
    global flag_Button_Launch

    if pin == pin_Flipper_Left:
        #write_report(xxx)
        flag_Flipper_Left = False        
    if pin == pin_Flipper_Right:
        #write_report(xxx)
        flag_Flipper_Right = False

    if pin == pin_Button_A:
        #write_report(xxx)
        flag_Button_A = False
    if pin == pin_Button_B:
        #write_report(xxx)
        flag_Button_B = False
    if pin == pin_Button_X:
        #write_report(xxx)
        flag_Button_X = False
    if pin == pin_Button_Y:
        #write_report(xxx)
        flag_Button_Y = False

    if pin == pin_Button_Launch:
        #write_report(xxx)
        flag_Button_Launch = False
        
    return


def report_Plunger(distance):
    #write_report(distance)
    return

if __name__ == '__main__':
    # your main function here
    # 1- first call init function
    init()
    # 2- looping infinitely 
    while True:
        #3- test if any of the callbacks shou happen
        
        if flag_Flipper_Left is True:
            report(pin_Flipper_Left)
            
        if flag_Flipper_Right is True:
            report(pin_Flipper_Right)

        if flag_Button_Launch is True:
            report(pin_Button_Launch)

        if flag_Button_A is True:
            report(pin_Button_A)

        if flag_Button_B is True:
            report(pin_Button_B)
        
        if flag_Button_X is True:
            report(pin_Button_X)

        if flag_Button_Y is True:
            report(pin_Button_Y)

        # only report a change if there's something to report 
        reportDistance = measure_plunger()
        if reportDistance == True:
            report_Plunger(plunger_distance)

    pass