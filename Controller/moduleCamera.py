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
            t =  round(6+ (self.angle/144) , 2)       
            print('Camera angle {} {}'.format(t , self.angle))
            self.VS.ChangeDutyCycle(t)
            sleep(0.2)
            self.VS.ChangeDutyCycle(0)                   
    
    def stop(self):
        self.stopped = True
        self.VS.ChangeDutyCycle(0)
        print('Camera Module stopped')



class CameraPID:
    def __init__(self):        
        xpin = 20
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        # GPIO.setup(xpin,GPIO.OUT)
        GPIO.setup(VERTICALSERVO,GPIO.OUT)

        # self.x=GPIO.PWM(xpin,50)
        self.y=GPIO.PWM(VERTICALSERVO,50)
        self.currentx,self.currenty=7,4        

    def start(self):
        # self.x.start(self.currentx)
        self.y.start(self.currenty)
        sleep(1)
        # self.x.ChangeDutyCycle(0)
        self.y.ChangeDutyCycle(0)
        return self

    # def setposx(self,diffx):
    #     self.currentx+=diffx
    #     self.currentx=round(self.currentx,2)
    #     if(self.currentx<15 and self.currentx>0):
    #         self.x.ChangeDutyCycle(self.currentx)

    def setposy(self,diffy):
        self.currenty+=diffy
        self.currenty=round(self.currenty,2)
        if(self.currenty<15 and self.currenty>0):
            self.y.ChangeDutyCycle(self.currenty)

    # def setdcx(self,dcx):
    #     self.x.ChangeDutyCycle(dcx)

    def setdcy(self,dcy):
        self.y.ChangeDutyCycle(dcy)
    
    def stop(self):
        # self.setdcx(0)
        self.setdcy(0)
        print('Camera Module stopped')