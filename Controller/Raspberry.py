from threading import Thread
from time import sleep
from Controller.moduleWheel import Wheel

class Raspberry:
    def __init__(self):
        self._adjustWheel = 'NOMOV'
        self._adjustCamera = 'NOMOV'
        self._isFaceDetected = False
        self.stopped = False
        self.wheel = Wheel().start()

    def start(self):
        Thread(name='moveCamera' , target=self.moveCamera).start()
        Thread(name='moveWheel' , target=self.moveWheel).start()
        return self

    def moveWheel(self):
        while not self.stopped:
            sleep(0.5)
            if self._isFaceDetected:
                if self._adjustWheel != 'NOMOV' :
                    print(self._adjustWheel)
                    self.wheel(self._adjustWheel)
            else:
                print('Stopped')

    def moveCamera(self):
        while not self.stopped:
            sleep(0.5)
            if self._isFaceDetected:
                if self._adjustCamera != 'NOMOV':
                    print(self._adjustCamera)
            else:
                print('Stopped')

    def setWheelCamera(self , wheel , camera):
        self._adjustCamera = camera
        self._adjustWheel = wheel

    def setFaceDetected(self , value):
        self._isFaceDetected = value

    def stop(self):
        self.wheel.stop()
        self.stopped = True            