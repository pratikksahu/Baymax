import logging
import socket
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
import threading
from threading import Thread
import re
import math
from picamera.array import PiRGBArray
from picamera import PiCamera

from flask import Response
from flask import render_template
from flask import Flask
from flask_ask import Ask, request, session, question, statement

app = Flask(__name__)
app_video = Flask("video_feed_display")
ask = Ask(app, "/")
logging.getLogger('flask_ask').setLevel(logging.DEBUG)
lock = threading.Lock()
outputFrame = None


@app_video.route("/")
def index():
    # return the rendered template
    return render_template("index.html")


def generate():
    # grab global references to the output frame and lock variables
    global outputFrame, lock
    # loop over frames from the output stream
    while True:
        # sleep(0.01)
        # wait until the lock is acquired
        with lock:
            # check if the output frame is available, otherwise skip
            # the iteration of the loop
            if outputFrame is None:
                continue
            # encode the frame in JPEG format
            (flag, encodedImage) = cv2.imencode(".jpg", outputFrame)
            # ensure the frame was successfully encoded
            if not flag:
                continue
        # yield the output frame in the byte format
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodedImage) + b'\r\n')


@app_video.route("/video_feed")
def video_feed():
    # return the response generated along with the specific media
    # type (mime type)
    return Response(generate(),
                    mimetype="multipart/x-mixed-replace; boundary=frame")


def start_flask():
    app.run(debug=True,
            threaded=True, use_reloader=False)


def start_flask_video(ipa):
    app_video.run(host=ipa, port=8000, debug=True,
                  threaded=True, use_reloader=False)


def on_press(key):
    global terminate
    if(key == Key.enter):
        terminate = True


def getIp():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    print("VIDEO FEED LINK - {}:8000".format(s.getsockname()[0]))
    return s.getsockname()[0]


def follow_face(source=0, dur=30):
    global lock, outputFrame
    print('Started for {} seconds'.format(dur))
    video_getter = None
    video_shower = None
    frameInfo = FrameInfo()
    facePoint = FacePoint()
    facePointTemp = FacePoint()
    startTime = datetime.now()
    currentTime = 0
    isSaving = True
    isFaceDetected = True
    # Get video feed from camera or video file
    video_getter = VideoGet().start()
    frameInfo = video_getter.frameInfo

    # camera initialize
    sleep(1)

    # Show processed video frame
    video_shower = VideoShow(
        video_getter.frame, video_getter.frameInfo, 'classifier/C10').start()
    facePoint = video_shower.facePoint

    # To Get moving commands
    movement = Movement(frameInfo=frameInfo).start()

    # To Send moving commands to raspberry
    raspberry = Raspberry().start()

    while True:
        # sleep(0.1)
        facePoint = video_shower.facePoint
        currentTime = (datetime.now() - startTime).seconds

        if(currentTime % dur == 0) and (currentTime != 0):
            print('Time up , Stopped')
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

        if facePoint != FacePoint():  # Initial startup when facepoint is (0,0,0,0)
            movement.setFaceDetected(isFaceDetected)
            raspberry.setFaceDetected(isFaceDetected)
            # Calculate directions only when face is in view
            movement.setFacePoint(facePoint)
            # Sending commands to raspberry
            raspberry.setWheelCamera(
                movement.adjustWheels(), movement.adjustCamera())

        frame = video_getter.frame
        video_shower.frame = frame

        with lock:
            outputFrame = video_shower.frame


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
    res = re.search(regex, str(duration))
    dur = 0
    if(res != None):
        res = res.group()
        unit = res[len(res) - 1]
        j = len(res) - 2
        for i in range(len(res) - 1):
            dur += int(int(res[i]) * math.pow(10, j))
            j = j - 1

        if(unit == 'M' or unit == 'H'):
            dur = dur*60
        unit = 'S'
    Thread(target=follow_face, args=[0, dur]).start()
    unit = 'Seconds'
    return question("Started following for {} {}".format(dur, unit))


@ask.intent('AMAZON.FallbackIntent')
def fallback():
    speech_text = 'You can say hello to me!'
    return question(speech_text).reprompt(speech_text).simple_card('HelloWorld', speech_text)


if __name__ == '__main__':
    if 'ASK_VERIFY_REQUESTS' in os.environ:
        verify = str(os.environ.get('ASK_VERIFY_REQUESTS', '')).lower()
        if verify == 'false':
            app.config['ASK_VERIFY_REQUESTS'] = False
            app_video.config['ASK_VERIFY_REQUESTS'] = False
    server_flask = Thread(target=start_flask)
    video_flask = Thread(target=start_flask_video, args=(getIp(),))

    server_flask.start()
    video_flask.start()
    server_flask.join()
    video_flask.join()
