from dataPointObject.dataPointObjectClass import *

class Controller:

    def __init__(self, frameInfo=FrameInfo()):
        self.facePoint = FacePoint()
        self.frameInfo = frameInfo
        self._isDetected = False
        self.stopped = False

    def start(self):
        print('Started')
        return self

    def sendCommand(self):
        self.drive()
        self.adjustCamera()

    def drive(self):
        if self._isDetected:
            if self.facePoint.x+self.facePoint.w > self.frameInfo.frameWidthLimitR:  # Right Screen Margin
                print('LEFT')
            elif self.facePoint.x < self.frameInfo.frameWidthLimitL:  # Left Screen Margin
                print('RIGHT')

    def adjustCamera(self):
        if self._isDetected:
            if self.facePoint.y < self.frameInfo.frameHeightLimitT:  # Top Screen Margin
                print('DOWN')
            elif self.facePoint.y + self.facePoint.h > self.frameInfo.frameHeightLimitB:  # Bottom Screen Margin
                print('UP')

    def stop(self):
        self._isDetected = False
        self.stopped = True

    def setFacePoint(self , facePoint):
        self.facePoint = facePoint

    def setFaceDetected(self , isDetected = False):
        self._isDetected = isDetected
