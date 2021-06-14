import RPi.GPIO as GPIO
from time import sleep
#17 Right Reverse
#18 Right Forward 12
#23 Left Forward  13
#24 Left Reverse

RR = 17
RF = 12
LF = 13
LR = 24

class Wheel:
    def __init__(self):
        
        print('Initializing Wheels')
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(RR,GPIO.OUT)
        GPIO.setup(RF,GPIO.OUT)
        GPIO.setup(LF,GPIO.OUT)
        GPIO.setup(LR,GPIO.OUT)

        GPIO.output(RR, False)
        GPIO.output(RF, False)
        GPIO.output(LF, False)
        GPIO.output(LR, False)

        self.RPWM=GPIO.PWM(RF,100)
        self.LPWM=GPIO.PWM(LF,100)

    def start(self):
        self.RPWM.start(0)
        self.LPWM.start(0)
        return self
        
    def move(self , direction):        
        if direction == 'FORWARD':
            self.forward(100)
        elif direction == 'RIGHT':
            self.right(100)
        elif direction == 'LEFT':
            self.left(100)
        elif direction == 'BACKWARD':
            self.reverse()
        elif direction == 'NOMOV':
            self.stop()


    def forward(self,speed):                
        self.RPWM.ChangeDutyCycle(speed)
        self.LPWM.ChangeDutyCycle(speed)
        GPIO.output(LR, False)
        GPIO.output(RR, False)
        GPIO.output(RF, True)
        GPIO.output(LF, True)

    def reverse(self):
        self.RPWM.ChangeDutyCycle(0)
        self.LPWM.ChangeDutyCycle(0)
        GPIO.output(RF, False)
        GPIO.output(LF, False)
        GPIO.output(RR, True)
        GPIO.output(LR, True)

    def right(self,speed):
        self.LPWM.ChangeDutyCycle(speed)
        GPIO.output(RR, False)
        GPIO.output(RF, False)
        GPIO.output(LR, False)
        GPIO.output(LF, True)
        sleep(0.1)

    def left(self,speed):
        self.RPWM.ChangeDutyCycle(speed)
        GPIO.output(RR, False)
        GPIO.output(LF, False)
        GPIO.output(LR, False)
        GPIO.output(RF, True)
        sleep(0.1)


    def stop(self):
        self.RPWM.ChangeDutyCycle(0)
        self.LPWM.ChangeDutyCycle(0)
        GPIO.output(RR, False)
        GPIO.output(RF, False)
        GPIO.output(LF, False)
        GPIO.output(LR, False)        

