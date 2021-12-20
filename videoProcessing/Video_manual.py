# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
from time import sleep
from dataClass.FrameInfo import FrameInfo
from dataClass.FacePoint import FacePoint
from threading import Thread

class VideoManual:
    def __init__(self , moduleCamera) -> None:
        self.frame = None
        self.stopped = False
        self._width = 640
        self._height = 480
        self._camera = moduleCamera        
        
    def start(self):
        self.y=self._camera.y
        self.currentY = 6
        self.y.start(self.currentY)
        sleep(1)
        self.y.ChangeDutyCycle(0)
        Thread(name='manual_mode', target=self.get).start()
        return self    
    
    def get(self):
        with PiCamera() as self.camera:
            self.camera.resolution = (self._width,self._height)
            self.camera.framerate = 30
            self.rawCapture = PiRGBArray(self.camera, size=(self._width,self._height))            

            for frame in self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True):
                image = frame.array                
                self.rawCapture.truncate(0)
                if self.stopped:
                    break
                self.frame=image
    
    def stop(self):
        self.stopped = True