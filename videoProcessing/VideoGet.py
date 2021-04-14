import threading
import cv2
from dataClass.FrameInfo import FrameInfo
from dataClass.FacePoint import FacePoint


class VideoGet:
    """
    Class that continuously gets frames from a VideoCapture object
    with a dedicated thread.
    """

    def __init__(self, src=0):

        #To change vertical margins
        self.verticalFactor = .2

        #To change horizontal margins
        self.horizontalFactor = .2
        if(src == 0):
            self.stream = cv2.VideoCapture(src, cv2.CAP_DSHOW)
        else:
            self.stream = cv2.VideoCapture(src)

        (self.grabbed, self.frame) = self.stream.read()
        self._width = self.stream.get(3) 
        self._height = self.stream.get(4)
        self.frameInfo = FrameInfo(frameWidth=int(self._width),
                                   frameWidthLimitR=int(self._width - self.horizontalFactor*self._width),
                                   frameWidthLimitL=int(self._width*self.horizontalFactor),
                                   frameHeight=int(self._height),
                                   frameHeightLimitB=int(self._height - self.verticalFactor*self._height),
                                   frameHeightLimitT=int(self.verticalFactor*self._height)
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
        self.stream.release()
