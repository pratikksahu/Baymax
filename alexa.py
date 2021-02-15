import logging
import os
from Controller.Movement import Movement
from Controller.Raspberry import Raspberry
import argparse
from dataClass.FrameInfo import FrameInfo
from dataClass.FacePoint import FacePoint
import os
import cv2
from time import sleep
from helper.CountsPerSec import CountsPerSec
from videoProcessing.VideoGet import VideoGet
from videoProcessing.VideoShow import VideoShow
from datetime import date, datetime
from threading import Thread
import re


from flask import Flask
from flask_ask import Ask, request, session, question, statement


app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger('flask_ask').setLevel(logging.DEBUG)



def putIterationsPerSec(frame, iteration_per_sec):
    cv2.putText(frame, '{:0.0f}'.format(iteration_per_sec),
                (10, 450), cv2.FONT_HERSHEY_COMPLEX, 0.6, (255, 255, 255))
    return frame


def follow_face(source=0 , dur = 30):
    print('Started for {} seconds'.format(dur))
    video_getter = None
    video_shower = None
    frameInfo = FrameInfo()
    facePoint = FacePoint()
    facePointTemp = FacePoint()
    startTime =  datetime.now()
    currentTime = 0
    isSaving = True
    isFaceDetected = True
    # Get video feed from camera or video file
    video_getter = VideoGet("videoProcessing/pewd.mp4").start()
    frameInfo = video_getter.frameInfo

    # Show processed video frame
    video_shower = VideoShow(
        video_getter.frame, video_getter.frameInfo).start()
    facePoint = video_shower.facePoint

    # To Get moving commands
    movement = Movement(frameInfo=frameInfo).start()

    # To Send moving commands to raspberryq
    raspberry = Raspberry().start()
    # FPS Counter
    cps = CountsPerSec().start()
    while True:
        sleep(0.01)
        facePoint = video_shower.facePoint

        currentTime = (datetime.now() - startTime).seconds

        if(currentTime % dur == 0) and (currentTime != 0):
            print('Stopped')
            video_shower.stop()
            video_getter.stop()
            movement.stop()
            raspberry.stop()
            break

        if (currentTime % 2 == 0) and (currentTime != 0):
            if isSaving:
                isSaving = False
                facePointTemp = facePoint

        if (currentTime % 2 != 0) and (currentTime != 0):
            if not isSaving:
                if facePointTemp == facePoint:
                    isFaceDetected = False
                else:
                    isFaceDetected = True
            isSaving = True

        movement.setFaceDetected(isFaceDetected)
        raspberry.setFaceDetected(isFaceDetected)
        # Calculate directions only when face is in view
        movement.setFacePoint(facePoint)
        # Sending commands to raspberry
        raspberry.setWheelCamera(
            movement.adjustWheels(), movement.adjustCamera())

        raspberry.moveCamera()
        raspberry.moveWheel()

        frame = video_getter.frame
        frame = putIterationsPerSec(frame, cps.countsPerSec())
        video_shower.frame = frame
        cps.increment()


@ask.launch
def launch():
    speech_text = 'Welcome to Raspberry Pi Automation.'
    return question(speech_text).reprompt(speech_text).simple_card(speech_text)


@ask.intent('GpioIntent', mapping={'status': 'status'})
def Gpio_Intent(status, room):
    return question('Lights turned {}'.format(status))

@ask.intent('followDuration', mapping={'duration': 'duration'})
def followDurationIntent(duration, room):
    regex = re.compile('[0-9]{1,}[HSM]{1}')
    res = re.search(regex,str(duration))
    dur = ''
    if(res != None):
        res = res.group()
        unit = res[len(res) - 1]
        for i in range(len(res) - 1):
            dur+=res[i]

        if(unit == 'M' or unit == 'H'):
            dur = int(dur)*60
        unit = 'S'
    Thread(target=follow_face , args=[0,dur]).start()
    unit = 'Seconds'
    return question("Started following for {} {}".format(dur,unit))


@ask.intent('AMAZON.FallbackIntent')
def fallback():
    speech_text = 'You can say hello to me!'
    return question(speech_text).reprompt(speech_text).simple_card('HelloWorld', speech_text)


if __name__ == '__main__':
    if 'ASK_VERIFY_REQUESTS' in os.environ:
        verify = str(os.environ.get('ASK_VERIFY_REQUESTS', '')).lower()
        if verify == 'false':
            app.config['ASK_VERIFY_REQUESTS'] = False
    app.run(debug=True)
