from threading import Thread


class Raspberry:
    def __init__(self):
        self._adjustWheel = 'NOMOV'
        self._adjustCamera = 'NOMOV'
        self._isFaceDetected = False
        self.stopped = False

    def start(self):
        return self

    def moveWheel(self):
        if self._isFaceDetected:
            if self._adjustWheel != 'NOMOV' :
                print(self._adjustWheel)
        else:
            print('Stopped')

    def moveCamera(self):
        if self._isFaceDetected:
            if self._adjustCamera != 'NOMOV':
                print(self._adjustCamera)
        else:
            print('Stopped')

    def setWheelCamera(self , wheel , camera):
        self._adjustCamera = camera
        self._adjustWheel = wheel

    def setFaceDetected(self , value = False):
        self._isFaceDetected = value

    def stop(self):
        self.stopped = True            