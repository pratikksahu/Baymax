import threading
import cv2
from dataClass.FrameInfo import FrameInfo
from dataClass.FacePoint import FacePoint
from time import sleep
from picamera.array import PiRGBArray
from picamera import PiCamera

class VideoGet:
    """
    Class that continuously gets frames from a VideoCapture object
    with a dedicated thread.
    """

    def __init__(self):

        #To change vertical margins
        self.verticalFactor = .2

        #To change horizontal margins
        self.horizontalFactor = .1

        self.camera = PiCamera()
        self.camera.resolution = (640, 480)
        self.camera.framerate = 32
        self.rawCapture = PiRGBArray(self.camera, size=(640, 480))


        self._width = 640
        self._height = 480
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
        for frame in self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True):
            if self.stopped:
                break
            self.frame = frame.array
            self.rawCapture.truncate(0)


    def stop(self):
        self.stopped = True
        self.camera.close()
