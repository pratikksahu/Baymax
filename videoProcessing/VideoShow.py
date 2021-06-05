import threading
import logging as log
import datetime as dt
from dataClass.FrameInfo import FrameInfo
from dataClass.FacePoint import FacePoint
import cv2


class VideoShow:
    """
    Class that continuously shows a frame using a dedicated thread.
    """

    def __init__(self, frame=None , frameInfo = FrameInfo()):
        self.faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.facePoint = FacePoint()
        self.frameInfo = frameInfo
        self.frame = frame
        self.stopped = False
        self.isFaceDetected = False

        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.recognizer.read('trainer.yml')
        self.names = ['None', 'Samiksha', 'Pratik']

    def start(self):
        threading.Thread(name='show',target=self.show).start()
        return self

    def show(self):
        while not self.stopped:
            gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)  
            faces = self.faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=6,
            minSize=(30,30)
            )

            if len(faces) > 0:
                self.isFaceDetected = True
            else:
                self.isFaceDetected = False

            # Draw Constraints in every frame irrespective of whether face has been detected or not
            cv2.putText(self.frame, ("Safe Area Line"), (self.frameInfo.frameWidthLimitL,
                                                         self.frameInfo.frameHeightLimitT - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255))
            cv2.rectangle(self.frame, (self.frameInfo.frameWidthLimitL, self.frameInfo.frameHeightLimitT),
                          (self.frameInfo.frameWidthLimitR, self.frameInfo.frameHeightLimitB), (255, 0, 0), 2)

            # Draw a rectangle around the faces
            for (x, y, w, h) in faces:
                # (startx , starty) (endx , endy)
                X = int(x)
                Y = int(y)
                W = int(w)
                H = int(h)
                CX = int((x+x+w)/2)
                CY = int((y+y+h)/2)

                id, confidence = self.recognizer.predict(gray[y:y+h,x:x+w])
                if (confidence < 100):
                        id = self.names[id]
                        confidence = "  {}-{}%".format(id,round(100 - confidence))
                        self.facePoint = FacePoint(X, Y, W, H, CX, CY)
                else:
                    id = "unknown"
                    confidence = "  {}-{}%".format(id,round(100 - confidence))
                # self.facePoint = FacePoint(X, Y, W, H, CX, CY)
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
            


    def stop(self):
        self.stopped = True
