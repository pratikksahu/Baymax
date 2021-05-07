import threading
import logging as log
import datetime as dt
from dataClass.FrameInfo import FrameInfo
from dataClass.FacePoint import FacePoint
import cv2

faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')


class VideoShow:
    """
    Class that continuously shows a frame using a dedicated thread.
    """

    def __init__(self, frame=None , frameInfo = FrameInfo()):
        self.facePoint = FacePoint()
        self.frameInfo = frameInfo
        self.frame = frame
        self.stopped = False

    def start(self):
        threading.Thread(name='show',target=self.show).start()
        return self

    def show(self):
        while not self.stopped:
            gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)  
            faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=6,
            minSize=(30,30)
            )

            #Draw Constraints in every frame irrespective of whether face has been detected or not
            cv2.putText(self.frame ,("Safe Area Line") , (self.frameInfo.frameWidthLimitL , self.frameInfo.frameHeightLimitT - 5) , cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255) )
            cv2.rectangle(self.frame, (self.frameInfo.frameWidthLimitL, self.frameInfo.frameHeightLimitT), (self.frameInfo.frameWidthLimitR, self.frameInfo.frameHeightLimitB), (255, 0, 0), 2)
            
            #Center point
            cv2.circle(self.frame,(int(self.frameInfo.frameWidth/2) , int(self.frameInfo.frameHeight/2)),6,(255,0,255),cv2.FILLED)

            # Draw a rectangle around the faces
            for (x, y, w, h) in faces:
                X = int(x)
                Y = int(y)
                W = int(w)
                H = int(h)
                CX = int((x+x+w)/2)
                CY = int((y+y+h)/2)

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

            #Reset points to 0
            if len(faces) == 0:
                self.facePoint = FacePoint()
            
            cv2.imshow("Video", self.frame)
            # cv2.imshow("Gray" , gray)
            if cv2.waitKey(1) == ord("q"):
                self.stopped = True


    def stop(self):
        self.stopped = True
