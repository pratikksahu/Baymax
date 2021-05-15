import RPi.GPIO as GPIO
from time import sleep


#Send GPIO output every 0.5 seconds
#17 Right Reverse
#18 Right Forward 12
#23 Left Forward  13
#24 Left Reverse

RR = 17
RF = 12
LF = 13
LR = 24

print('Initializing Wheels')
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(RR,GPIO.OUT)
GPIO.setup(RF,GPIO.OUT)
GPIO.setup(LF,GPIO.OUT)
GPIO.setup(LR,GPIO.OUT)

GPIO.output(RR, False)
GPIO.output(RF, False)
GPIO.output(LF, False)
GPIO.output(LR, False)

RPWM=GPIO.PWM(RF,100)
LPWM=GPIO.PWM(LF,100)

print('Starting PWM')
RPWM.start(0)
LPWM.start(0)
sleep(2)

def forward(speed):
    #Forward
    print('Moving Forward {}'.format(speed))
    RPWM.ChangeDutyCycle(speed)
    LPWM.ChangeDutyCycle(speed)
    GPIO.output(LR, False)
    GPIO.output(RR, False)
    GPIO.output(RF, True)
    GPIO.output(LF, True)
    sleep(3)

def reverse():
    #Reverse
    print('Moving Backward')
    RPWM.ChangeDutyCycle(0)
    LPWM.ChangeDutyCycle(0)
    GPIO.output(RF, False)
    GPIO.output(LF, False)
    GPIO.output(RR, True)
    GPIO.output(LR, True)
    sleep(3)

def right(speed):
    #Right
    print('Moving Right {}'.format(speed))    
    LPWM.ChangeDutyCycle(speed)
    GPIO.output(RR, False)
    GPIO.output(RF, False)
    GPIO.output(LR, False)
    GPIO.output(LF, True)
    sleep(3)

def left(speed):
    #Left
    print('Moving Left {}'.format(speed))
    RPWM.ChangeDutyCycle(speed)
    GPIO.output(RR, False)
    GPIO.output(LF, False)
    GPIO.output(LR, False)
    GPIO.output(RF, True)
    sleep(3)    

def stop():
    #Stop
    print('Stopped')
    RPWM.ChangeDutyCycle(0)
    LPWM.ChangeDutyCycle(0)
    GPIO.output(RR, False)
    GPIO.output(RF, False)
    GPIO.output(LF, False)
    GPIO.output(LR, False)

print('Forward Speed 100')
forward(100)
stop()

print('Forward Speed 50')
forward(50)
stop()

print('Right Speed 100')
right(100)
stop()

print('Right Speed 20')
right(20)
stop()

print('Left Speed 100')
left(100)
stop()

print('Left Speed 20')
left(20)
stop()

print('Reverse Speed 100')
reverse()
stop()
