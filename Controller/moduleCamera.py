import RPi.GPIO as GPIO
from time import sleep
from threading import Thread
import math

#Servo Pin 18

TILTSERVO = 18
PANSERVO = 19


class CameraPID():
    def __init__(self):
        print('Initialising PANTILT Module..')
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(PANSERVO,GPIO.OUT)
        GPIO.setup(TILTSERVO,GPIO.OUT)

        self.x=GPIO.PWM(PANSERVO,50)
        self.y=GPIO.PWM(TILTSERVO,50)
        self.currentx,self.currenty=7,4
        self.x.start(self.currentx)
        self.y.start(self.currenty)
        sleep(1)
        self.x.ChangeDutyCycle(0)
        self.y.ChangeDutyCycle(0)
        print('PANTILT Module initialised successfully')
            
    def setposx(self,diffx):
        self.currentx+=diffx
        self.currentx=round(self.currentx,2)
        if(self.currentx<15 and self.currentx>0):
            self.x.ChangeDutyCycle(self.currentx)  

    def setposy(self,diffy):
        self.currenty+=diffy
        self.currenty=round(self.currenty,2)
        if(self.currenty<15 and self.currenty>0):
            self.y.ChangeDutyCycle(self.currenty)  

    def setdcx(self,dcx):
        self.x.ChangeDutyCycle(dcx)  

    def setdcy(self,dcy):
        self.y.ChangeDutyCycle(dcy)

    def stop(self):
        self.setdcx(0)
        self.setdcy(0)
        print('Camera Module stopped')
