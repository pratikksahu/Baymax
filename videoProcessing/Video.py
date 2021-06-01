# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
from time import sleep
import cv2
from dataClass.FrameInfo import FrameInfo
from dataClass.FacePoint import FacePoint
from threading import Thread
import RPi.GPIO as GPIO


TILTSERVO = 18
PANSERVO = 19


class Video:
    def __init__(self):
        # To change vertical margins
        self.verticalFactor = .2

        #To change horizontal margins
        self.horizontalFactor = .3


        self._width = 640
        self._height = 480
        self.frameInfo = FrameInfo(frameWidth=int(self._width),
                                   frameWidthLimitR=int(
                                       self._width - self.horizontalFactor*self._width),
                                   frameWidthLimitL=int(
                                       self._width*self.horizontalFactor),
                                   frameHeight=int(self._height),
                                   frameHeightLimitB=int(
                                       self._height - self.verticalFactor*self._height),
                                   frameHeightLimitT=int(
                                       self.verticalFactor*self._height),
                                       frameCX=int(self._width/2),
                                       frameCY=int(self._height/2)
                                   )
        
        self.face_cascade= cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        #PID variables
        self.Px,self.Ix,self.Dx= -2/self.frameInfo.frameCX,0,0
        self.Py,self.Iy,self.Dy= -0.4/self.frameInfo.frameCY,0,0
        self.integral_x,self.integral_y=0,0
        self.differential_x,self.differential_y=0,0
        self.prev_x,self.prev_y=0,0

        self.stopped = False

        #Accessible Variables
        self.frame = None
        self.isFaceDetected = False
        self.facePoint = FacePoint()
        

    def start(self):
        print('Initialising PANTILT Module..')
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(PANSERVO,GPIO.OUT)
        GPIO.setup(TILTSERVO,GPIO.OUT)

        self.x=GPIO.PWM(PANSERVO,50)
        self.y=GPIO.PWM(TILTSERVO,50)
        self.currentx,self.currenty=7,5
        self.x.start(self.currentx)
        self.y.start(self.currenty)
        sleep(1)
        self.x.ChangeDutyCycle(0)
        self.y.ChangeDutyCycle(0)
        print('PANTILT Module initialised successfully')

        print('Starting camera....')
        Thread(name='show', target=self.get).start()
        sleep(2)
        print('Camera Initialised successfully.')
        return self

    def get(self):
        with PiCamera() as self.camera:
            self.camera.resolution = (self._width,self._height)
            self.camera.framerate = 30
            self.rawCapture = PiRGBArray(self.camera, size=(self._width,self._height))            

            for frame in self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True):
                image = frame.array
                # self.frame=cv2.flip(image,1)
                self.frame=image
                gray=cv2.cvtColor(self.frame,cv2.COLOR_BGR2GRAY)    

                self.y.ChangeDutyCycle(0)
                # self.x.ChangeDutyCycle(0)

                #detect face coordinates x,y,w,h
                faces=self.face_cascade.detectMultiScale(gray,1.3,5)

                if len(faces) > 0:
                    self.isFaceDetected = True
                else:
                    self.isFaceDetected = False
                #Draw Constraints in every frame irrespective of whether face has been detected or not
                cv2.putText(self.frame ,("Safe Area Line") , (self.frameInfo.frameWidthLimitL , self.frameInfo.frameHeightLimitT - 5) , cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255) )
                # cv2.rectangle(self.frame, (self.frameInfo.frameWidthLimitL, self.frameInfo.frameHeightLimitT), (self.frameInfo.frameWidthLimitR, self.frameInfo.frameHeightLimitB), (255, 0, 0), 2)
                cv2.line(self.frame, (self.frameInfo.frameWidthLimitL, self.frameInfo.frameHeightLimitT), (self.frameInfo.frameWidthLimitL, self.frameInfo.frameHeightLimitB), (255, 0, 0), 2)
                cv2.line(self.frame, (self.frameInfo.frameWidthLimitR, self.frameInfo.frameHeightLimitT), (self.frameInfo.frameWidthLimitR, self.frameInfo.frameHeightLimitB), (255, 0, 0), 2)

                #Center point
                cv2.circle(self.frame,(int(self.frameInfo.frameWidth/2) , int(self.frameInfo.frameHeight/2)),6,(255,0,255),cv2.FILLED)
                c = 0
                for(x,y,w,h) in faces:
                    c= c + 1
                    if c >1:
                        break                    
                    X = int(x)
                    Y = int(y)
                    W = int(w)
                    H = int(h)
                    CX = int(x+ (w/2))
                    CY = int(y+ (h/2))
    
                    self.facePoint = FacePoint(X, Y, W, H, CX, CY)
                    # Show Coordinates with width and height of face detected
                    cv2.putText(self.frame, ("X:{} Y:{} W:{} H:{}".format(
                        x, y, w, h)), (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255))
                    cv2.rectangle(self.frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    # X Axis
                    cv2.line(self.frame, (int(CX), int(CY)),
                             (0, int(CY)), (0, 0, 255), 2)
                    # Y Axis
                    cv2.line(self.frame, (int(CX), int(CY)),
                             (int(CX), 0), (0, 0, 255), 2)                        
                    #centre of face
                    face_centre_x=CX
                    face_centre_y=CY

                    #pixels to move 
                    error_x=self.frameInfo.frameCX-face_centre_x
                    error_y=self.frameInfo.frameCY-face_centre_y

                    self.integral_x=self.integral_x+error_x
                    self.integral_y=self.integral_y+error_y

                    self.differential_x= self.prev_x- error_x
                    self.differential_y= self.prev_y- error_y

                    self.prev_x=error_x
                    self.prev_y=error_y

                    valx=self.Px*error_x +self.Dx*self.differential_x + self.Ix*self.integral_x
                    valy=self.Py*error_y +self.Dy*self.differential_y + self.Iy*self.integral_y


                    valx=round(valx,2)
                    valy=round(valy,2)                    

                    # if abs(error_x)<20:
                    #     self.CameraPID.setdcx(0)
                    # else:
                    #     if abs(valx)>0.5:
                    #         sign=valx/abs(valx)
                    #         valx=0.5*sign
                    #     self.currentx+=valx
                    #     self.currentx=round(self.currentx,2)
                    #     if(self.currentx<15 and self.currentx>0):
                    #         self.x.ChangeDutyCycle(self.currentx)              

                    if abs(error_y)<20:
                        self.y.ChangeDutyCycle(0)
                    else:
                        if abs(valy)>0.5:
                            sign=valy/abs(valy)
                            valy=0.5*sign
                        self.currenty+=valy
                        self.currenty=round(self.currenty,2)
                        if(self.currenty<15 and self.currenty>0):
                            self.y.ChangeDutyCycle(self.currenty)  

                # cv2.imshow('frame',self.frame) #display image

                # key = cv2.waitKey(1) & 0xFF
                self.rawCapture.truncate(0)
                if self.stopped:
                    break
                # if key == ord("q"):
                #     break
                
            # cv2.destroyAllWindows()

    def stop(self):
        self.stopped = True