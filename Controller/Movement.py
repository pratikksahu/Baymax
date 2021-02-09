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
        self.isFaceDetected = False
        self.stopped = False
        self._startTime = datetime.now()
        self._currentTime = 0
        self._thread = Thread(target=self.isDetected)

    def start(self):
        print('Started')
        # self._thread.start()
        return self

    def isDetected(self):
        while not self.stopped:
            self._currentTime = (datetime.now() - self._startTime).seconds
            if self._currentTime % 2 == 0:
                self._facePointTemp = self.facePoint
            
            if self._currentTime % 3 == 0:
                if self._facePointTemp == self.facePoint:
                    self.isFaceDetected = False
                else:
                    self.isFaceDetected = True


    def adjustWheels(self):
        if self.facePoint.x+self.facePoint.w > self.frameInfo.frameWidthLimitR:  # Right Screen Margin
            return 'RIGHT'
        elif self.facePoint.x < self.frameInfo.frameWidthLimitL:  # Left Screen Margin
            return 'LEFT'
        return 'NOMOV'

    def adjustCamera(self):

        if self.facePoint.y < self.frameInfo.frameHeightLimitT:  # Top Screen Margin
            return 'DOWN'
        elif self.facePoint.y + self.facePoint.h > self.frameInfo.frameHeightLimitB:  # Bottom Screen Margin
            return 'UP'
        return 'NOMOV'


    def setFacePoint(self , facePoint):
        self.facePoint = facePoint

    def stop(self):
        self.stopped = True