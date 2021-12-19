import RPi.GPIO as GPIO
from time import sleep

TILTSERVO = 18
PANSERVO = 19

class Camera:
    def __init__(self):
        
        print('Initializing PANTILT MODULE...')
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(PANSERVO,GPIO.OUT)
        GPIO.setup(TILTSERVO,GPIO.OUT)
        
        self.x = GPIO.PWM(PANSERVO,50)
        self.y = GPIO.PWM(TILTSERVO,50)

    def start(self):
        return self


    def stop(self):
        self.x.ChangeDutyCycle(0)
        self.y.ChangeDutyCycle(0)   

