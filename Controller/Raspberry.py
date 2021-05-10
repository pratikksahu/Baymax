from threading import Thread


class Raspberry:
    def __init__(self):
        self._adjustWheel = 'NOMOV'
        self._adjustCamera = 0
        self.stopped = False

    def start(self):
        return self

    def moveWheel(self):
        if self._adjustWheel != 'NOMOV':
            print(self._adjustWheel)

    def moveCamera(self):
        if self._adjustCamera != 0:
            print(self._adjustCamera)    

    def setWheelCamera(self , wheel , camera):
        self._adjustCamera = camera
        self._adjustWheel = wheel

    def stop(self):
        self.stopped = True            