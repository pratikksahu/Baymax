import time
import RPi.GPIO as GPIO
from threading import Thread


#Send GPIO output every 0.5 seconds
#17 Right Reverse
#18 Right Forward 12
#23 Left Forward  13
#24 Left Reverse


class Wheel:
    def __init__(self):
        
        print('Initializing Wheels')
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(17,GPIO.OUT)
        GPIO.setup(12,GPIO.OUT)
        GPIO.setup(13,GPIO.OUT)
        GPIO.setup(24,GPIO.OUT)

        GPIO.output(17, False)
        GPIO.output(12, False)
        GPIO.output(13, False)
        GPIO.output(24, False)

        self.RPWM=GPIO.PWM(12,100)
        self.LPWM=GPIO.PWM(13,100)

    def start(self):
        self.RPWM.start(0)
        self.LPWM.start(0)
        return self
        
    def move(self):
        if direction == 'FORWARD':
            self.forward(100)
        elif direction == 'RIGHT':
            self.right(20)
        elif direction == 'LEFT':
            self.left(20)
        elif direction == 'BACKWARD':
            self.reverse()
        elif direction == 'NOMOV':
            self.stop()


    def forward(speed):                
        self.RPWM.ChangeDutyCycle(speed)
        self.LPWM.ChangeDutyCycle(speed)
        GPIO.output(24, False)
        GPIO.output(17, False)
        GPIO.output(12, True)
        GPIO.output(13, True)

    def reverse():
        self.RPWM.ChangeDutyCycle(0)
        self.LPWM.ChangeDutyCycle(0)
        GPIO.output(12, False)
        GPIO.output(13, False)
        GPIO.output(17, True)
        GPIO.output(24, True)

    def right(speed):
        self.LPWM.ChangeDutyCycle(speed)
        GPIO.output(17, False)
        GPIO.output(12, False)
        GPIO.output(24, False)
        GPIO.output(13, True)

    def left(speed):
        self.RPWM.ChangeDutyCycle(speed)
        GPIO.output(17, False)
        GPIO.output(13, False)
        GPIO.output(24, False)
        GPIO.output(12, True)


    def stop():
        self.RPWM.ChangeDutyCycle(0)
        self.LPWM.ChangeDutyCycle(0)
        GPIO.output(17, False)
        GPIO.output(12, False)
        GPIO.output(13, False)
        GPIO.output(24, False)

