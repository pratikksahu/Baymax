import threading
import cv2
from dataPointObject.dataPointObjectClass import FrameInfo


class VideoGet:
    """
    Class that continuously gets frames from a VideoCapture object
    with a dedicated thread.
    """

    def __init__(self, src=0):
        self.verticalFactor = .2
        self.horizontalFactor = .1
        if(src == 0):
            self.stream = cv2.VideoCapture(src, cv2.CAP_DSHOW)
        else:
            self.stream = cv2.VideoCapture(src)

        (self.grabbed, self.frame) = self.stream.read()
        self.frameInfo = FrameInfo(frameWidth=int(self.stream.get(3)),
                                   frameWidthLimitR=int(self.stream.get(
                                       3) - self.horizontalFactor*self.stream.get(3)),
                                   frameWidthLimitL=int(
                                       self.stream.get(3)*self.horizontalFactor),
                                   frameHeight=int(self.stream.get(4)),
                                   frameHeightLimitB=int(self.stream.get(
                                       4) - self.verticalFactor*self.stream.get(4)),
                                   frameHeightLimitT=int(
                                       self.verticalFactor*self.stream.get(4))
                                   )
        self.stopped = False

    def start(self):
        threading.Thread(name='get', target=self.get).start()
        return self

    def get(self):
        while not self.stopped:
            if not self.grabbed:
                self.stop()
            else:
                (self.grabbed, self.frame) = self.stream.read()

    def stop(self):
        self.stopped = True
