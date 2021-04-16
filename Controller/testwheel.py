import RPi.GPIO as GPIO
from time import sleep


#Send GPIO output every 0.5 seconds
#17 Right Reverse
#18 Right Forward
#23 Left Forward
#24 Left Reverse

print('Initializing Wheels')
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(17,GPIO.OUT)
GPIO.setup(18,GPIO.OUT)
GPIO.setup(23,GPIO.OUT)
GPIO.setup(24,GPIO.OUT)

GPIO.output(17, False)
GPIO.output(18, False)
GPIO.output(23, False)
GPIO.output(24, False)

self.RPWM=GPIO.PWM(18,100)
self.LPWM=GPIO.PWM(23,100)

print('Starting PWM')
self.RPWM.start(100)
self.LPWM.start(100)
sleep(2)

print('Changing Duty cycle to 0')
self.RPWM.ChangeDutyCycle(0)
self.LPWM.ChangeDutyCycle(0)
sleep(2)

print('Changing Duty cycle to 20')
self.RPWM.ChangeDutyCycle(20)
self.LPWM.ChangeDutyCycle(20)
sleep(2)

print('Changing Duty cycle to 80')
self.RPWM.ChangeDutyCycle(80)
self.LPWM.ChangeDutyCycle(80)
sleep(2)


def forward(speed):
    #Forward
    print('Moving Forward {}'.format(speed))
    self.RPWM.ChangeDutyCycle(speed)
    self.LPWM.ChangeDutyCycle(speed)
    GPIO.output(24, False)
    GPIO.output(17, False)
    GPIO.output(18, True)
    GPIO.output(23, True)
    sleep(3)

def reverse():
    #Reverse
    print('Moving Backward')
    self.RPWM.ChangeDutyCycle(0)
    self.LPWM.ChangeDutyCycle(0)
    GPIO.output(18, False)
    GPIO.output(23, False)
    GPIO.output(17, True)
    GPIO.output(24, True)
    sleep(3)

def right(speed):
    #Right
    print('Moving Right {}'.format(speed))    
    self.LPWM.ChangeDutyCycle(speed)
    GPIO.output(17, False)
    GPIO.output(18, False)
    GPIO.output(24, False)
    GPIO.output(23, True)
    sleep(3)

def left(speed):
    #Left
    print('Moving Left {}'.format(speed))
    self.RPWM.ChangeDutyCycle(speed)
    GPIO.output(17, False)
    GPIO.output(23, False)
    GPIO.output(24, False)
    GPIO.output(18, True)
    sleep(3)    

def stop():
    #Stop
    print('Stopped')
    self.RPWM.ChangeDutyCycle(0)
    self.LPWM.ChangeDutyCycle(0)
    GPIO.output(17, False)
    GPIO.output(18, False)
    GPIO.output(23, False)
    GPIO.output(24, False)


stop()
reverse()
stop()
forward(100)
stop()
forward(50)
stop()
right(100)
stop()
right(50)
stop()
left(100)
stop()
left(50)
stop()
reverse()
stop()

