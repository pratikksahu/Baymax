import time
import RPi.GPIO as GPIO
from threading import Thread

#Send GPIO output every 0.5 seconds

class Wheel:
    def __init__(self):
        direction
        print('Initializing Wheels')
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(True)
        GPIO.setup(17,GPIO.OUT)
        GPIO.setup(18,GPIO.OUT)
        GPIO.setup(23,GPIO.OUT)
        GPIO.setup(24,GPIO.OUT)

        GPIO.output(17, False)
        GPIO.output(24, False)
        GPIO.output(18, False)
        GPIO.output(23, False)

    def move(self , direction):
        if direction == 'FORWARD':
            self.forward()
        if direction == 'RIGHT':
            self.right()
        if direction == 'LEFT':
            self.left()
        if direction == 'REVERSE':
            self.reverse()

    def forward(self):
        GPIO.output(17, True)
        GPIO.output(24, True)
        GPIO.output(18, True)
        GPIO.output(24, True)

    def reverse(self):
        GPIO.output(17, False)
        GPIO.output(24, False)
        GPIO.output(18, False)
        GPIO.output(24, False)

    def right(self):
        GPIO.output(17, True)
        GPIO.output(24, True)
        GPIO.output(18, False)
        GPIO.output(24, False)

    def left(self):
        GPIO.output(17, False)
        GPIO.output(24, False)
        GPIO.output(18, True)
        GPIO.output(24, True)


    def stop(self):
        GPIO.output(17, False)
        GPIO.output(24, False)
        GPIO.output(18, False)
        GPIO.output(24, False)
        quit()
