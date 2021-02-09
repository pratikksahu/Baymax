from dataClass.FrameInfo import FrameInfo
from dataClass.FacePoint import FacePoint
from datetime import datetime
from threading import Thread
#Used to get movements for camera and

class Movement:

    def __init__(self, frameInfo=FrameInfo()):
        self.facePoint = FacePoint()
        self._facePointTemp = FacePoint()
        self.frameInfo = frameInfo
        self._isFaceDetected = False
        self.stopped = False

    def start(self):
        print('Started')
        return self


    def adjustWheels(self):
        if self._isFaceDetected :
            if self.facePoint.x+self.facePoint.w > self.frameInfo.frameWidthLimitR:  # Right Screen Margin
                return 'RIGHT'
            elif self.facePoint.x < self.frameInfo.frameWidthLimitL:  # Left Screen Margin
                return 'LEFT'
            return 'NOMOV'

    def adjustCamera(self):
        if self._isFaceDetected :
            if self.facePoint.y < self.frameInfo.frameHeightLimitT:  # Top Screen Margin
                return 'DOWN'
            elif self.facePoint.y + self.facePoint.h > self.frameInfo.frameHeightLimitB:  # Bottom Screen Margin
                return 'UP'
            return 'NOMOV'


    def setFaceDetected(self , value = False):
        self._isFaceDetected = value

    def setFacePoint(self , facePoint):
        self.facePoint = facePoint

    def stop(self):
        self.stopped = True