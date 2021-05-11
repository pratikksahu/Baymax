from threading import Thread
from time import sleep
from Controller.moduleWheel import Wheel
from Controller.moduleCamera import Camera

class Raspberry:
    def __init__(self , moduleWheel , moduleCamera):
        self._adjustWheel = 'NOMOV'
        self._adjustCamera = 0
        self._isFaceDetected = False
        self.stopped = False
        self.moduleWheel = moduleWheel      
        self.moduleCamera = moduleCamera  
        # self.moduleCamera.initThread()

    def start(self):
        Thread(name='moveCamera' , target=self.moveCamera).start()
        Thread(name='moveWheel' , target=self.moveWheel).start()
        return self

    def moveWheel(self):
        pass
        # while not self.stopped:            
        #     if self._isFaceDetected:
        #         if self._adjustWheel != None:                                        
        #             self.moduleWheel.move(self._adjustWheel)      
        #     else:
        #         self.moduleWheel.move('NOMOV')
                
    def moveCamera(self):
        while not self.stopped:            
            if self._isFaceDetected:
                self.moduleCamera.move(self._adjustCamera)

    def setWheelCamera(self , wheel , camera):
        self._adjustCamera = camera
        self._adjustWheel = wheel

    def setFaceDetected(self , value):
        self._isFaceDetected = value

    def stop(self):
        self.moduleWheel.stop()
        self.moduleCamera.stop()
        self.stopped = True     
    
