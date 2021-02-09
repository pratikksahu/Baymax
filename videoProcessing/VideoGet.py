import threading
import cv2
from dataClass.FrameInfo import FrameInfo
from dataClass.FacePoint import FacePoint
from imutils.video import VideoStream
import imutils


class VideoGet:
    """
    Class that continuously gets frames from a VideoCapture object
    with a dedicated thread.
    """

    def __init__(self, src=0):
        self.verticalFactor = .2
        self.horizontalFactor = .1
        if(src == 0):
            self.vs = VideoStream(0).start()
        else:
            self.vs = VideoStream(src).start()
        print(self.vs.frame)
        self.frame = self.vs.read()
        self.frame = imutils.resize(self.frame, width=480 , height=640)
        self.frameInfo = FrameInfo()
        # self.frameInfo = FrameInfo(frameWidth=int(self.frame.get(3)),
        #                            frameWidthLimitR=int(self.frame.get(
        #                                3) - self.horizontalFactor*self.frame.get(3)),
        #                            frameWidthLimitL=int(
        #                                self.frame.get(3)*self.horizontalFactor),
        #                            frameHeight=int(self.frame.get(4)),
        #                            frameHeightLimitB=int(self.frame.get(
        #                                4) - self.verticalFactor*self.frame.get(4)),
        #                            frameHeightLimitT=int(
        #                                self.verticalFactor*self.frame.get(4))
        #                            )
        self.stopped = False

    def start(self):
        threading.Thread(name='get', target=self.get).start()
        return self

    def get(self):
        while not self.stopped:
            self.frame = self.vs.read()
            self.frame = imutils.resize(self.frame, width=480 , height=640)
    def stop(self):
        self.stopped = True
