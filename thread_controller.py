from dataPointObject.dataPointObjectClass import *
import threading


class Drive:

    def __init__(self, frameInfo=FrameInfo()):
        self.facePoint = PointFace()
        self.obstaclePoint = PointObstacle()
        self.frameInfo = frameInfo
        self.isDetected = False
        self.stopped = False

    def start(self):
        print('Started')
        # multiprocessing.Process(target = self.drive).start()
        # multiprocessing.Process(target=self.adjustCamera).start()
        threading.Thread(name='Drive', target=self.drive).start()
        threading.Thread(name='AdjustCamera', target=self.adjustCamera).start()
        return self

    def drive(self):
        while not self.stopped:
            while self.isDetected:
                if self.facePoint.x+self.facePoint.w > self.frameInfo.frameWidthLimitR:  # Right Screen Margin
                    print('LEFT')
                elif self.facePoint.x < self.frameInfo.frameWidthLimitL:  # Left Screen Margin
                    print('RIGHT')

    def adjustCamera(self):
        while not self.stopped:
            while self.isDetected:
                if self.facePoint.y < self.frameInfo.frameHeightLimitT:  # Top Screen Margin
                    print('DOWN')
                elif self.facePoint.y + self.facePoint.h > self.frameInfo.frameHeightLimitB:  # Bottom Screen Margin
                    print('UP')

    def stop(self):
        self.isDetected = False
        self.stopped = True

    def faceDetected(self , isDetected = False):
        self.isDetected = isDetected
