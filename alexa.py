import logging
import socket
import os
from videoProcessing.Video_manual import VideoManual
from Controller.Movement import Movement
from Controller.Raspberry import Raspberry
from Controller.moduleWheel import Wheel
import argparse
from dataClass.FrameInfo import FrameInfo
from dataClass.FacePoint import FacePoint
import cv2
from time import sleep
from videoProcessing.Video import Video
from videoProcessing.video_line import VideoLine
from datetime import date, datetime
import threading
from threading import Thread
import re
from Controller.moduleWheel import Wheel
from flask import Response
from flask import render_template
from flask import Flask , make_response , redirect , request , url_for
from flask_ask import Ask, request, session, question, statement
import click
import math
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials



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
video_flag = 1 # 1 for just video , 2 for video with face detection
VIDEO_FEED_IP = ""
manual_mode = 0
STATUSON = ['on','high']
STATUSOFF = ['off','low']
wheel = Wheel().start()
events= None


@app_video.route("/")
def index():
    global video_flag
    # return the rendered template
    return render_template("index.html" , video_flag=video_flag)


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


@app_video.route('/<direction>', methods=['POST'])
def move_robot(direction):
    global  video_flag , manual_mode , wheel    
    if manual_mode == 1:
        if direction == "1":   
            wheel.move('FORWARD')
        if direction == "4":   
            wheel.move('RIGHT')
        if direction == "3":   
            wheel.move('LEFT')
        if direction == "2":   
            wheel.move('BACKWARD')
        if direction == "5":   
            wheel.move('NOMOV')    
    return render_template("index.html" , video_flag=video_flag)
    # response = make_response(redirect(url_for('index')))
    # return(response)

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

def manualmode(dur=30):
    global video_flag,outputFrame,manual_mode , wheel
    
    print('Manual Mode Started')   
    video_manual = None
    video_manual = VideoManual().start()
    video_flag = 1
    startTime = datetime.now()
    currentTime = 0

    while True:
        currentTime = (datetime.now() - startTime).seconds            
        if((currentTime % dur == 0) and (currentTime != 0)) or manual_mode == 0:
            video_manual.stop()
            manual_mode = 0
            sleep(1)          
            print('Manual Mode Stopped')      
            break                    
        outputFrame = video_manual.frame


@ask.intent('manualmode', mapping={'status': 'status'})
def Gpio_Intent(status, room):
    global manual_mode
    if status in STATUSON:
        manual_mode = 1
        Thread(target=manualmode, args=[100]).start()
        return statement('Manual Mode turned {} for 30 seconds'.format(status))
    if status in STATUSOFF:
        manual_mode = 0
        return statement('Manual Mode turned {}'.format(status))

def follow_line(dur):
    global outputFrame, wheelDirectionHTML
    videoline = VideoLine(wheel).start()
    startTime = datetime.now()
    currentTime = 0

    while True:
        currentTime = (datetime.now() - startTime).seconds            
        if((currentTime % dur == 0) and (currentTime != 0)):
            videoline.stop()
            sleep(1)          
            print('Path follow Stopped')      
            break 
        with lockDirection:                
                w = videoline.adjustWheels()
                if w != None:
                    wheelDirectionHTML = w
        outputFrame = videoline.frame

def follow_face(dur=30):
    global outputFrame, camDirectionHTML, wheelDirectionHTML, facePointHTML,lockDirection,video_flag,wheel
    print('Started for {} seconds'.format(dur))    
    video_flag = 2
    video = None    
    
    facePoint = FacePoint()    
    startTime = datetime.now()
    currentTime = 0
    isFaceDetected = False    

    video = Video().start()

    facePoint = video.facePoint
    frameInfo = video.frameInfo
    # To Get moving commands
    movement = Movement(frameInfo=frameInfo).start()


    # To Send moving commands to raspberry
    raspberry = Raspberry(wheel).start()
    try:

        while True:
            facePoint = video.facePoint
            currentTime = (datetime.now() - startTime).seconds
            
            if(currentTime % dur == 0) and (currentTime != 0):
                raspberry.stop()
                movement.stop()                                
                video.stop()
                print('Stopped following')
                sleep(1)                
                wheel.stop()
                break
            
            isFaceDetected = video.isFaceDetected
            if not isFaceDetected:
                facePoint = FacePoint()
            # Calculate directions only when face is in view
            movement.setFacePoint(facePoint)

            movement.setFaceDetected(isFaceDetected)
            raspberry.setFaceDetected(isFaceDetected)
            
            # Sending commands to raspberry
            raspberry.setWheelCamera(
                movement.adjustWheels())

            with lockDirection:
                c = video.currenty
                w = movement.adjustWheels()
                if c != None:
                    camDirectionHTML = c
                if w != None:
                    wheelDirectionHTML = w
                facePointHTML = facePoint
            
            outputFrame = video.frame
    except KeyboardInterrupt:
        raspberry.stop()
        movement.stop()
        wheel.stop()                
        video.stop()


@ask.launch
def launch():
    speech_text = 'Hello , My name is baymax.'
    return question(speech_text).reprompt(speech_text).simple_card(speech_text)


@ask.intent('lights', mapping={'status': 'status'})
def Gpio_Intent(status, room):
    return question('Lights turned {}'.format(status))


@ask.intent('alarm', mapping={'time': 'time'})
def Gpio_Intent(time, room):
    return question('Alarm set for {}'.format(time))

@ask.intent('followDuration', mapping={'duration': 'duration'})
def followDurationIntent(duration, room):
    global manual_mode
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
    if manual_mode == 0:
        #Add +2 seconds to compensate camera initialisation time
        Thread(target=follow_face, args=[dur+2]).start()
        unit = 'Seconds'
        return statement("Started following for {} {}".format(dur, unit))
    else:
        return statement("Please disable manual mode first")    

@ask.intent('calender_event')
def calender_eventIntent():
    global events
    e=""
    if not events:
        print('No upcoming events found.')
        e="No upcoming events found."
        return statement(e)    

    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])
        e= e+event['summary']+"\n"
    
    return statement(e)




def fetch_event():
    global events
    creds = None
    SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    while True:
        
        now = datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
        print('Getting the upcoming 10 events')
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
        events = events_result.get('items', [])
        sleep(20)


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
    Thread(target=follow_line , args=[60,]).start()
    # Thread(target=follow_face, args=[1000]).start()
    # Thread(target=fetch_event).start()
    server_flask = Thread(target=start_flask)
    video_flask = Thread(target=start_flask_video, args=(getIp(),))

    server_flask.start()
    video_flask.start()
    server_flask.join()
    video_flask.join()
