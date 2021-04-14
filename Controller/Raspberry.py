from threading import Thread
from time import sleep

class Raspberry:
    def __init__(self):
        self._adjustWheel = 'NOMOV'
        self._adjustCamera = 'NOMOV'
        self._isFaceDetected = False
        self.stopped = False
        self.delay = 0.002

    def start(self):
        Thread(name='moveCamera' , target=self.moveCamera).start()
        Thread(name='moveWheel' , target=self.moveWheel).start()
        return self

    def moveWheel(self):
        while not self.stopped:
            # sleep(self.delay)
            if self._isFaceDetected:
                if self._adjustWheel != None:        
                    pass            
                    # print(self._adjustWheel)
            # else:
            #     print('Stopped')

    def moveCamera(self):
        while not self.stopped:
            # sleep(self.delay)
            if self._isFaceDetected:
                if  self._adjustCamera != None:
                    pass
                    # print(self._adjustCamera)
            # else:
            #     print('Stopped')
                
    def setWheelCamera(self , wheel , camera):
        self._adjustCamera = camera
        self._adjustWheel = wheel

    def setFaceDetected(self , value):
        self._isFaceDetected = value

    def stop(self):
        self.stopped = True            