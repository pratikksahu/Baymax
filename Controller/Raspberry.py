from threading import Thread
from time import sleep
from Controller.moduleWheel import Wheel

class Raspberry:
    def __init__(self , moduleWheel):
        self._adjustWheel = 'NOMOV'
        self._adjustCamera = 'NOMOV'
        self._isFaceDetected = False
        self.stopped = False
        self.moduleWheel = moduleWheel

    def start(self , ):
        Thread(name='moveCamera' , target=self.moveCamera).start()
        Thread(name='moveWheel' , target=self.moveWheel).start()
        return self

    def moveWheel(self):
        while not self.stopped:
            sleep(0.05)
            if self._isFaceDetected:
                # print(self._adjustWheel)
                self.moduleWheel.move(self._adjustWheel)                
            else:
                # print('Stopped')
                self.moduleWheel.move('NOMOV')

    def moveCamera(self):
        while not self.stopped:
            sleep(0.05)
            if self._isFaceDetected:
                if self._adjustCamera != 'NOMOV':
                    # print(self._adjustCamera)
            else:
                pass
                # print('Stopped')

    def setWheelCamera(self , wheel , camera):
        self._adjustCamera = camera
        self._adjustWheel = wheel

    def setFaceDetected(self , value):
        self._isFaceDetected = value

    def stop(self):
        self.wheel.stop()
        self.stopped = True     
    