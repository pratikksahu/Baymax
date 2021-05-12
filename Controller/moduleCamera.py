import RPi.GPIO as GPIO
from time import sleep
from threading import Thread

#Servo Pin 18

VERTICALSERVO = 18


class Camera:
    def __init__(self):
        print('Initialising Camera')
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(VERTICALSERVO,GPIO.OUT)
        self.VS = GPIO.PWM(VERTICALSERVO,50)
        self.angle = 0        
        self.stopped = False

    def start(self):
        self.VS.start(0)
        self.VS.ChangeDutyCycle(4)        
        self.VS.ChangeDutyCycle(0)        
        Thread(name='setAngle' , target=self.setAngle).start()
        return self

    def move(self , angle):
        if not angle == 0:
            self.angle = angle
    
    def setAngle(self):        
        while not self.stopped:                            
            self.VS.ChangeDutyCycle(4+(self.angle/18))
            sleep(0.2)
            self.VS.ChangeDutyCycle(0)
            sleep(0.3) 
    
    def stop(self):
        self.stopped = True
        self.VS.ChangeDutyCycle(0)
        print('Camera Module stopped')