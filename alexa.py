import logging
import socket
import os
from Controller.Movement import Movement
from Controller.Raspberry import Raspberry
from Controller.moduleWheel import Wheel
import argparse
from dataClass.FrameInfo import FrameInfo
from dataClass.FacePoint import FacePoint
import cv2
from time import sleep
from helper.CountsPerSec import CountsPerSec
from videoProcessing.VideoGet import VideoGet
from videoProcessing.VideoShow import VideoShow
from datetime import date, datetime
import threading
from threading import Thread
import re
from flask import Response
from flask import render_template
from flask import Flask
from flask_ask import Ask, request, session, question, statement
import click


app = Flask(__name__)
app_video = Flask("video_feed_display")
ask = Ask(app, "/")

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


def secho(text, file=None, nl=None, err=None, color=None, **styles):
    pass


def echo(text, file=None, nl=None, err=None, color=None, **styles):
    pass


click.echo = echo
click.secho = secho

lock = threading.Lock()
lockDirection = threading.Lock()
outputFrame = None
camDirectionHTML = "Waiting for face"
wheelDirectionHTML = "Waiting for face"
facePointHTML = FacePoint()

VIDEO_FEED_IP = ""


@app_video.route("/")
def index():
    # return the rendered template
    return render_template("index.html")


@app.route("/")
def indexURL():
    return render_template("videofeedip.html")


def generate():
    # grab global references to the output frame and lock variables
    global outputFrame
    # loop over frames from the output stream
    while True:
        # wait until the lock is acquired       
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


@app_video.route("/information")
def image_information():

    def yieldInformation():

        global wheelDirectionHTML, camDirectionHTML, facePointHTML , lockDirection

        with lockDirection:  
            yield '<b> <br> FacePoint: {}<br> Camera: {} <br> Wheel: {}</b>'.format(facePointHTML, camDirectionHTML, wheelDirectionHTML)

    return Response(yieldInformation(), mimetype="text/event-stream")


def start_flask():
    app.run(debug=True,
            threaded=True, port=5000, use_reloader=False)


def start_flask_video(ipa):
    app_video.run(host=ipa, port=8000, debug=True,
                  threaded=True, use_reloader=False)


def setIp():
    global VIDEO_FEED_IP
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    VIDEO_FEED_IP = s.getsockname()[0]


def getIp():
    global VIDEO_FEED_IP
    print("VIDEO FEED LINK - http://{}:8000".format(VIDEO_FEED_IP))
    return VIDEO_FEED_IP



@app.route("/videofeedip")
def videofeedip():
    def yieldIP():
        yield "<h1> https://{}:8000 </h1>".format(getIp())

    return Response(yieldIP(), mimetype="text/event-stream")


def follow_face(source=0, dur=30):
    global outputFrame, camDirectionHTML, wheelDirectionHTML, facePointHTML,lockDirection
    print('Started for {} seconds'.format(dur))
    video_getter = None
    video_shower = None
    frameInfo = FrameInfo()
    facePoint = FacePoint()
    facePointTemp = FacePoint()
    startTime = datetime.now()
    currentTime = 0
    isFaceDetected = False
    isSaving = False
    # Get video feed from camera or video file
    video_getter = VideoGet().start()
    frameInfo = video_getter.frameInfo

    # Initialize camera
    sleep(2)

    # Show processed video frame
    video_shower = VideoShow(
        video_getter.frame, video_getter.frameInfo, 'classifier/C10').start()

    facePoint = video_shower.facePoint

    # To Get moving commands
    movement = Movement(frameInfo=frameInfo).start()

    # To prevent GPIO setup everytime
    moduleWheel = Wheel().start()
    # To Send moving commands to raspberry
    raspberry = Raspberry(moduleWheel).start()
    try:

        while True:
            facePoint = video_shower.facePoint
            currentTime = (datetime.now() - startTime).seconds
            # print((datetime.now() - startTime).microseconds / 1000)
            if(currentTime % dur == 0) and (currentTime != 0):
                moduleWheel.stop()
                raspberry.stop()
                movement.stop()                
                video_shower.stop()
                video_getter.stop()
                print('Time up , Stopped')
                break
            
            isFaceDetected = video_shower.isFaceDetected
            if not isFaceDetected:
                facePoint = FacePoint()
            #  # Save latest facepoints every odd seconds
            # if round(float(currentTime) % 1.5, 2) != 0 and (round(float(currentTime) % 1.5, 2) == 1.0 or round(float(currentTime) % 1.5, 2) == 0.0):
            #     if isSaving:
            #         isSaving = False
            #         facePointTemp = facePoint
            # # every even second , check whether current facepoint
            # # matches the prev facepoint , if its same then most probably no face is detected
            # # else face is still in frame and detected
            # if round(float(currentTime) % 1.5, 2) != 0 and round(float(currentTime) % 1.5, 2) == 0.5:
            #     if not isSaving:
            #         if facePointTemp == facePoint:
            #             isFaceDetected = False
            #         else:
            #             isFaceDetected = True
            #     isSaving = True
            
            movement.setFaceDetected(isFaceDetected)
            raspberry.setFaceDetected(isFaceDetected)
            # Calculate directions only when face is in view
            movement.setFacePoint(facePoint)
            # Sending commands to raspberry
            raspberry.setWheelCamera(
                movement.adjustWheels(), movement.adjustCamera())

            with lockDirection:
                c = movement.adjustCamera()
                w = movement.adjustWheels()
                if c != None:
                    camDirectionHTML = c
                if w != None:
                    wheelDirectionHTML = w
                facePointHTML = facePoint

            frame = video_getter.frame
            video_shower.frame = frame
            outputFrame = video_shower.frame
    except KeyboardInterrupt:
        raspberry.stop()
        movement.stop()
        moduleWheel.stop()
        video_shower.stop()
        video_getter.stop()


@ask.launch
def launch():
    speech_text = 'Hello , My name is baymax.'
    return question(speech_text).reprompt(speech_text).simple_card(speech_text)


@ask.intent('GpioIntent', mapping={'status': 'status'})
def Gpio_Intent(status, room):
    return question('Lights turned {}'.format(status))


@ask.intent('alarm', mapping={'time': 'time'})
def Gpio_Intent(time, room):
    return question('Alarm set for {}'.format(time))


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

    #Add +2 seconds to compensate camera initialisation time
    Thread(target=follow_face, args=[0, dur+2]).start()
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
    setIp()
    
    
    server_flask = Thread(target=start_flask)
    video_flask = Thread(target=start_flask_video, args=(getIp(),))

    server_flask.start()
    video_flask.start()
    server_flask.join()
    video_flask.join()
