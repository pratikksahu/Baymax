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
from flask import Response
from flask import Flask
from flask import render_template
import threading
from pynput.keyboard import Key, Listener


# Argument parser
ap = argparse.ArgumentParser()
ap.add_argument("--source", "-s", default=0,
                help="Path to video file or integer representing webcam index"
                + " (default 0).")
ap.add_argument("--classifier", "-c", required=True,
                help="Path to classifier")
ap.add_argument("--ip", "-ip", required=True,
                help="IP address for stream")
ap.add_argument("--port", "-p", required=True,
                help="Port for respected IP address")
args = vars(ap.parse_args())
###################################################

# python main.py -c classifier/C10 -ip 192.168.29.53 -p 8000

frameInfo = FrameInfo()
facePoint = FacePoint()
video_getter = None
video_shower = None
facePointTemp = FacePoint()
currentTime = 0
startTime = datetime.now()
lock = threading.Lock()
outputFrame = None
terminate = False
app = Flask(__name__)

@app.route("/")
def index():
    # return the rendered template
    return render_template("index.html")


def generate():
    # grab global references to the output frame and lock variables
    global outputFrame, lock
    # loop over frames from the output stream
    while True:
        sleep(0.01)
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


@app.route("/video_feed")
def video_feed():
    # return the response generated along with the specific media
    # type (mime type)
    return Response(generate(),
                    mimetype="multipart/x-mixed-replace; boundary=frame")


def start_flask():
    app.run(host=args["ip"], port=int(args["port"]), debug=True,
            threaded=True, use_reloader=False)
    

def on_press(key):
    global terminate
    if(key == Key.enter):
        terminate = True


def start(source=0):

    global video_getter, video_shower, frameInfo, facePoint, moveDirection, facePointTemp, startTime, currentTime, lock, outputFrame,terminate
    isSaving = True
    isFaceDetected = True
    # Get video feed from camera or video file
    video_getter = VideoGet(source).start()
    frameInfo = video_getter.frameInfo

    # Show processed video frame
    video_shower = VideoShow(
        video_getter.frame, video_getter.frameInfo, args['classifier']).start()
    facePoint = video_shower.facePoint

    # To Get moving commands
    movement = Movement(frameInfo=frameInfo).start()

    # To Send moving commands to raspberry
    raspberry = Raspberry().start()

    while True:
        sleep(0.1)
        facePoint = video_shower.facePoint
        currentTime = (datetime.now() - startTime).seconds
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
        if facePoint != FacePoint(): #Initial startup when facepoint is (0,0,0,0)
            movement.setFaceDetected(isFaceDetected)
            raspberry.setFaceDetected(isFaceDetected)
            # Calculate directions only when face is in view
            movement.setFacePoint(facePoint)
            # Sending commands to raspberry
            raspberry.setWheelCamera(
                movement.adjustWheels(), movement.adjustCamera())

        # if video_getter.stopped or video_shower.stopped:
        if terminate:
            
            video_getter.stop()
            video_shower.stop()
            movement.stop()
            raspberry.stop()
            break


        frame = video_getter.frame
        video_shower.frame = frame

        with lock:
            outputFrame = video_shower.frame


def main():

    # If source is a string consisting only of integers, check that it doesn't
    # refer to a file. If it doesn't, assume it's an integer camera ID and
    # convert to int.
    if (
        isinstance(args["source"], str)
        and args["source"].isdigit()
        and not os.path.isfile(args["source"])
    ):
        args["source"] = int(args["source"])
    start(args["source"])



if __name__ == "__main__":
    threading.Thread(target=start_flask).start()
    keyListener = Listener(on_press=on_press)
    keyListener.start()
    main()
