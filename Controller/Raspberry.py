from threading import Thread
from time import sleep
from Controller.moduleWheel import Wheel


class Raspberry:
    def __init__(self , moduleWheel):
        self._adjustWheel = 'NOMOV'        
        self._isFaceDetected = False
        self.stopped = False
        self.moduleWheel = moduleWheel                

    def start(self):        
        Thread(name='moveWheel' , target=self.moveWheel).start()
        return self

    def moveWheel(self):            
        while not self.stopped:            
            if self._isFaceDetected:
                if self._adjustWheel != None:                                        
                    self.moduleWheel.move(self._adjustWheel)      
            else:
                self.moduleWheel.move('NOMOV')
    
                

    def setWheelCamera(self , wheel):        
        self._adjustWheel = wheel

    def setFaceDetected(self , value):
        self._isFaceDetected = value

    def stop(self):
        self.moduleWheel.stop()        
        self.stopped = True     
    
