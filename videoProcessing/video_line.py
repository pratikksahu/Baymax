# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
from time import sleep
from threading import Thread
import numpy as np
import cv2
import RPi.GPIO as GPIO
from Controller.moduleWheel import Wheel

TILTSERVO = 18
PANSERVO = 19


class VideoLine:
    def __init__(self , moduleWheel , moduleCamera) -> None:
        self.frame = None
        self.stopped = False
        self._width = 160
        self._height = 128
        self._wheel = moduleWheel
        self._camera = moduleCamera
        self.move = ''
        
        
    def start(self):        
        self.x=self._camera.x
        self.y=self._camera.y
        self.currentx,self.currenty=7,12
        self.x.start(self.currentx)
        self.y.start(self.currenty)
        sleep(1)
        self.x.ChangeDutyCycle(0)
        self.y.ChangeDutyCycle(0)
        print('PANTILT Module initialised successfully') 
        Thread(name='video_line', target=self.get).start()  
        return self
    
    def get(self):
        with PiCamera() as self.camera:
            self.camera.resolution = (self._width,self._height)
            self.camera.framerate = 30
            self.rawCapture = PiRGBArray(self.camera, size=(self._width,self._height))            

            for frame in self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True):
                image = frame.array

                  # Crop the image
                crop_img = image[60:self._height, 0:self._width]

     # Convert to grayscale
                gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)

    # Gaussian blur
                blur = cv2.GaussianBlur(gray,(5,5),0)

    # Color thresholding
                ret,thresh1 = cv2.threshold(blur,60,255,cv2.THRESH_BINARY_INV)

    # Erode and dilate to remove accidental line detections
                mask = cv2.erode(thresh1, None, iterations=2)
                mask = cv2.dilate(mask, None, iterations=2)

    # Find the contours of the frame
                contours,hierarchy = cv2.findContours(mask.copy(), 1, cv2.CHAIN_APPROX_NONE)

                   # Find the biggest contour (if detected)
                if len(contours) > 0:
                    c = max(contours, key=cv2.contourArea)
                    M = cv2.moments(c)

                    cx = int(M['m10']/M['m00'])
                    cy = int(M['m01']/M['m00'])                    
                    cv2.line(crop_img,(cx,0),(cx,720),(255,0,0),1)
                    cv2.line(crop_img,(0,cy),(1280,cy),(255,0,0),1)

                    cv2.drawContours(crop_img, contours, -1, (0,255,0), 1)                    
                    if cx >= 95 :
                        self.move = 'RIGHT'                        
                        self.adjustWheels(self.move,50)
                    elif cx < 95 and cx > 40:                    
                        self.move = 'FORWARD'
                        self.adjustWheels(self.move ,100)
                    elif cx <= 30:
                        self.move = 'LEFT'                        
                        self.adjustWheels(self.move,50)
            

                else:
                        self.move = 'NOMOV'
                        self.adjustWheels(self.move)                                          


                self.rawCapture.truncate(0)
                if self.stopped:
                    break

                self.frame = crop_img
    def adjustWheels(self,movement,speed = 20):
        self._wheel.move(movement,speed)

    def getWheels(self):
        return self.move

    def stop(self):
        self._wheel.stop()
        self.stopped = True
