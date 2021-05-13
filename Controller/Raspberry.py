from threading import Thread
from time import sleep
from Controller.moduleWheel import Wheel
from Controller.moduleCamera import Camera
from Controller.moduleCamera import CameraPID

class Raspberry:
    def __init__(self , moduleWheel , moduleCamera):
        self._adjustWheel = 'NOMOV'
        self._adjustCamera = 0,0
        self._isFaceDetected = False
        self.stopped = False
        self.moduleWheel = moduleWheel      
        self.moduleCamera = moduleCamera          

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
                a,b = self._adjustCamera

                #Tilt
                if(b == 0):
                    self.moduleCamera.setdcy(b)
                else:
                    self.moduleCamera.setposy(b)
                    
                #Pan
                # if(a == 0):
                #     self.moduleCamera.setdcx(a)
                # else:
                #     self.moduleCamera.setposx(a)
                

    def setWheelCamera(self , wheel , camera):
        self._adjustCamera = camera
        self._adjustWheel = wheel

    def setFaceDetected(self , value):
        self._isFaceDetected = value

    def stop(self):
        self.moduleWheel.stop()
        self.moduleCamera.stop()
        self.stopped = True     
    
