from dataClass.FrameInfo import FrameInfo
from dataClass.FacePoint import FacePoint
import math



def calculateAngle(facePoint , frameInfo):
    srcX = frameInfo.frameCX
    srcY = frameInfo.frameCY
    destX = facePoint.cx
    destY = facePoint.cy
    P = srcY - destY
    B = srcX
    rad = math.atan(P/B)
    deg = math.floor(round(math.degrees(rad),1))
    return deg

class Movement:

    def __init__(self, frameInfo=FrameInfo()):
        self.facePoint = FacePoint()
        self.frameInfo = frameInfo
        self._isFaceDetected = False
        self.stopped = False
        self._forwardLimit = 9000
        self._backwardLimit = 20500

    def start(self):
        print('Started')
        return self


    def adjustWheels(self):
        faceArea = self.facePoint.w*self.facePoint.h
        if self._isFaceDetected :
            if self.facePoint.cx > self.frameInfo.frameWidthLimitR:  # Right Screen Margin
                return 'RIGHT'
            elif self.facePoint.cx < self.frameInfo.frameWidthLimitL:  # Left Screen Margin
                return 'LEFT'
            if faceArea < self._forwardLimit:     
                return 'FORWARD'
            if faceArea >self._backwardLimit:                    
                return 'BACKWARD'
            return 'NOMOV'
        return 'NOMOV'

    def adjustCamera(self):
        if self._isFaceDetected :
            t =  calculateAngle(self.facePoint , self.frameInfo)
            print('from calArea {}'.format(t))
            return t
        return 0

    def setFaceDetected(self , isFaceDetected = False):
        self._isFaceDetected = isFaceDetected

    def setFacePoint(self , facePoint):
        self.facePoint = facePoint

    def stop(self):
        self.stopped = True