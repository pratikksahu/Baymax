import time
import RPi.GPIO as GPIO
from threading import Thread


#Send GPIO output every 0.5 seconds
#17 Right Reverse
#18 Right Forward
#23 Left Forward
#24 Left Reverse


class Wheel:
    def __init__(self):
        
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

    def start(self):
        return self
        
    def move(self , direction):
        if direction == 'FORWARD':
            self.forward()
        elif direction == 'RIGHT':
            self.right()
        elif direction == 'LEFT':
            self.left()
        elif direction == 'BACKWARD':
            self.reverse()
        elif direction == 'NOMOV':
            self.stop()


    def forward(self):
        self.RPWM.ChangeDutyCycle(100)
        self.LPWM.ChangeDutyCycle(100)
        GPIO.output(24, False)
        GPIO.output(17, False)
        GPIO.output(18, True)
        GPIO.output(23, True)

    def reverse(self):
        GPIO.output(18, False)
        GPIO.output(23, False)
        GPIO.output(17, True)
        GPIO.output(24, True)

    def right(self):    
        self.LPWM.ChangeDutyCycle(10)
        GPIO.output(17, False)
        GPIO.output(18, False)
        GPIO.output(24, False)
        GPIO.output(23, True)

    def left(self):
        self.RPWM.ChangeDutyCycle(10)
        GPIO.output(17, False)
        GPIO.output(23, False)
        GPIO.output(24, False)
        GPIO.output(18, True)


    def stop(self):
        GPIO.output(17, False)
        GPIO.output(18, False)
        GPIO.output(23, False)
        GPIO.output(24, False)

