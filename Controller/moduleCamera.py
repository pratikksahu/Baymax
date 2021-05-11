import RPi.GPIO as GPIO
from time import sleep

#Servo Pin 18
# 160 > 18
# -160 < 18

VERTICALSERVO = 18


class Camera:
    def __init__(self):
        print('Initialising Camera')
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(VERTICALSERVO,GPIO.OUT)
        self.VS = GPIO.PWM(VERTICALSERVO,50)
        self.oldAngle = 0
        self.newAngle = 0
    
    def start(self):
        self.VS.start(0)
        return self
    
    def move(self , angle):
        if not angle == 90:
            self.newAngle = angle
            if not (self.oldAngle == self.newAngle) :
                self.setAngle(angle)
                self.oldAngle = self.newAngle
    
    def setAngle(self):
        self.VS.ChangeDutyCycle(2+(angle/18))
        sleep(0.3)
        self.VS.ChangeDutyCycle(0)
        sleep(1)
    
    def stop(self):
        self.VS.ChangeDutyCycle(0)
        print('Camera Module stopped')