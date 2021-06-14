# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
from time import sleep
from threading import Thread
import numpy as np
import cv2
import RPi.GPIO as GPIO

TILTSERVO = 18
PANSERVO = 19


class VideoLine:
    def __init__(self) -> None:
        self.frame = None
        self.stopped = False
        self._width = 640
        self._height = 480
        
        
    def start(self):
        print('Initialising PANTILT Module..')
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(PANSERVO,GPIO.OUT)
        GPIO.setup(TILTSERVO,GPIO.OUT)

        self.x=GPIO.PWM(PANSERVO,50)
        self.y=GPIO.PWM(TILTSERVO,50)
        self.currentx,self.currenty=7,10
        self.x.start(self.currentx)
        self.y.start(self.currenty)
        sleep(1)
        self.x.ChangeDutyCycle(0)
        self.y.ChangeDutyCycle(0)
        print('PANTILT Module initialised successfully') 
        Thread(name='manual_mode', target=self.get).start()  
    
    def get(self):
        with PiCamera() as self.camera:
            self.camera.resolution = (self._width,self._height)
            self.camera.framerate = 30
            self.rawCapture = PiRGBArray(self.camera, size=(self._width,self._height))            

            for frame in self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True):
                image = frame.array
                self.frame=image

                  # Crop the image
                crop_img = self.frame[60:self._height, 0:self._width]

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

                    if cx >= self._height:
                        print('right')

                    if cx < self._height and cx > 150:
                        print("stop")
                    if cx <= 50:
                        print("left")

                else:
                        print("forward")


                self.rawCapture.truncate(0)
                if self.stopped:
                    break

                            #Display the resulting frame
                cv2.imshow('frame',crop_img)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
    
    def stop(self):
        self.stopped = True

t = VideoLine().start()