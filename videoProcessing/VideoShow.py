import threading
import logging as log
import datetime as dt
from dataClass.FrameInfo import FrameInfo
from dataClass.FacePoint import FacePoint
import cv2

cascPath = "Classifier\haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)


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
            # gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(
            self.frame,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30,30)
            )

            #Draw Constraints in every frame irrespective of whether face has been detected or not
            cv2.putText(self.frame ,("Safe Area Line") , (self.frameInfo.frameWidthLimitL , self.frameInfo.frameHeightLimitT - 5) , cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255) )
            cv2.rectangle(self.frame, (self.frameInfo.frameWidthLimitL, self.frameInfo.frameHeightLimitT), (self.frameInfo.frameWidthLimitR, self.frameInfo.frameHeightLimitB), (255, 0, 0), 2)
            
            # Draw a rectangle around the faces
            for (x, y, w, h) in faces:
                self.facePoint = FacePoint(x,y,w,h)
                #Show Coordinates with width and height of face detected
                cv2.putText(self.frame ,("X:{} Y:{} W:{} H:{}".format(x,y,w,h)) , (x , y-5) , cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255) )
                cv2.rectangle(self.frame, (x, y), (x+w, y+h), (0, 255, 0), 2)


            #Reset points to 0
            if len(faces) == 0:
                self.facePoint = FacePoint()
            
            cv2.imshow("Video", self.frame)
            # cv2.imshow("Gray" , gray)
            if cv2.waitKey(1) == ord("q"):
                self.stopped = True


    def stop(self):
        self.stopped = True
