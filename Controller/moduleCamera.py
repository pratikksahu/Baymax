import RPi.GPIO as GPIO

#Servo Pin 18

VERTICALSERVO = 18


class Camera:
    def __init__(self):
        print('Initialising Camera')
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(VERTICALSERVO,GPIO.OUT)
        self.VS = GPIO.PWM(VERTICALSERVO,50)
    
    def start(self):
        self.VS.start(0)
        return self
    
    def move(self , angle):
        self.setAngle(angle)
    
    def setAngle(slef,angle):
        self.VS.ChangeDutyCycle(2+(angle/18))
        time.sleep(0.5)
        self.VS.ChangeDutyCycle(0)
    
    def stop(self):
        self.VS.ChangeDutyCycle(0)
        print('Camera Module stopped')