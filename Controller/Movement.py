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

        #PID Variables
        self.Px,self.Ix,self.Dx=-1/self.frameInfo.frameCX,0,0
        self.Py,self.Iy,self.Dy=-0.2/self.frameInfo.frameCY,0,0
        self.integral_x,self.integral_y=0,0
        self.differential_x,self.differential_y=0,0
        self.prev_x,self.prev_y=0,0

    def start(self):
        print('Started')
        return self

    def calculateAnglePID(self,facePoint , frameInfo):
        error_x = frameInfo.frameCX - facePoint.cx
        error_y = frameInfo.frameCY - facePoint.cy

        self.integral_x = self.integral_x + error_x
        self.integral_y = self.integral_y + error_y

        self.differential_x = self.prev_x - error_x
        self.differential_y = self.prev_y - error_y

        self.prev_x = error_x
        self.prev_y = error_y
        
        val_x=self.Px*error_x +self.Dx*self.differential_x + self.Ix*self.integral_x
        val_y=self.Py*error_y +self.Dy*self.differential_y + self.Iy*self.integral_y
        
        return_x = 0
        return_y = 0

        if abs(error_x)<20:
            return_x = 0
        else:
            if abs(val_x)>0.5:
                sign=val_x/abs(val_x)
                val_x=0.5*sign   
            return_x = val_x

        if abs(error_y)<20:            
            return_y = 0
        else:
            if abs(val_y)>0.5:
                sign=val_y/abs(val_y)
                val_y=0.5*sign
            return_y = val_y        


        return return_x,return_y        

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
            return self.calculateAnglePID(self.facePoint , self.frameInfo)
        return 0,0    

    def setFaceDetected(self , isFaceDetected = False):
        self._isFaceDetected = isFaceDetected

    def setFacePoint(self , facePoint):
        self.facePoint = facePoint

    def stop(self):
        self.stopped = True