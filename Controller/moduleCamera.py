import RPi.GPIO as GPIO
from time import sleep
from threading import Thread
import math

#Servo Pin 18

VERTICALSERVO = 18


class Camera:
    def __init__(self):
        print('Initialising Camera')
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(VERTICALSERVO,GPIO.OUT)
        self.VS = GPIO.PWM(VERTICALSERVO,50)
        self.angle = 0        
        self.oldAngle = 0
        self.stopped = False

    def start(self):
        self.VS.start(0)
        self.VS.ChangeDutyCycle(6)
        sleep(0.1)
        self.VS.ChangeDutyCycle(0)                
        return self

    def move(self , angle):
        if not angle == 0:
            if not self.oldAngle == angle:
                self.angle = angle
                self.setAngle()
                self.oldAngle = self.angle  
    
    def setAngle(self):                
        if not self.angle == None:
            t =  round(6+ (self.angle/18) , 2)       
            print('Camera angle {} {}'.format(t , self.angle))
            self.VS.ChangeDutyCycle(t)
            sleep(0.5)
            self.VS.ChangeDutyCycle(0)                       
    
    def stop(self):
        self.stopped = True
        self.VS.ChangeDutyCycle(0)
        print('Camera Module stopped')