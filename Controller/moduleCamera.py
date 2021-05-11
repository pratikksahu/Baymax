import RPi.GPIO as GPIO
from time import sleep

#Servo Pin 18

VERTICALSERVO = 18


class Camera:
    def __init__(self):
        print('Initialising Camera')
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(VERTICALSERVO,GPIO.OUT)
        self.VS = GPIO.PWM(VERTICALSERVO,50)
    
    def start(self):
        self.VS.start(0)
        return self
    
    def move(self , angle):
        self.setAngle(angle)

    def setAngle(self,angle):
        self.VS.ChangeDutyCycle(7+(angle/18))
        sleep(0.5)
        self.VS.ChangeDutyCycle(0)
        sleep(0.5)
    
    def stop(self):
        self.VS.ChangeDutyCycle(0)
        print('Camera Module stopped')