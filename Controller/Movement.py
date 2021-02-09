from dataClass.FrameInfo import FrameInfo
from dataClass.FacePoint import FacePoint


#Used to get movements for camera and

class Movement:

    def __init__(self, frameInfo=FrameInfo()):
        self.facePoint = FacePoint()
        self.frameInfo = frameInfo
        self.isFaceDetected = False
        self.stopped = False

    def start(self):
        print('Started')
        return self


    def adjustWheels(self):
        if self.isFaceDetected:
            if self.facePoint.x+self.facePoint.w > self.frameInfo.frameWidthLimitR * 2:  # Right Screen Margin
                return 'LEFT'
            elif self.facePoint.x < self.frameInfo.frameWidthLimitL * 2:  # Left Screen Margin
                return 'RIGHT'
        return 'NOMOV'

    def adjustCamera(self):
        if self.isFaceDetected:
            if self.facePoint.y < self.frameInfo.frameHeightLimitT * 2:  # Top Screen Margin
                return 'DOWN'
            elif self.facePoint.y + self.facePoint.h > self.frameInfo.frameHeightLimitB * 2:  # Bottom Screen Margin
                return 'UP'
        return 'NOMOV'

    def setFaceDetected(self , isFaceDetected = False):
        self.isFaceDetected = isFaceDetected

    def setFacePoint(self , facePoint):
        self.facePoint = facePoint

    def stop(self):
        self.stopped = True