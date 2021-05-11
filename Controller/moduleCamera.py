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
        Thread(name='setAngle' , target=self.setAngle).start()
        return self    

    def initThread(self):
        Thread(name='setAngle' , target=self.setAngle).start()

    def move(self , angle):        
        self.angle = angle
    
    def setAngle(self):
        while not self.stopped:
            self.VS.ChangeDutyCycle(7+(self.angle/18))
            sleep(0.1)
            self.VS.ChangeDutyCycle(0)
            sleep(0.1)
    
    def stop(self):
        self.stopped = True
        self.VS.ChangeDutyCycle(0)
        print('Camera Module stopped')