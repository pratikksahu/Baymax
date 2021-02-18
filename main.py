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

# Argument parser
ap = argparse.ArgumentParser()
ap.add_argument("--source", "-s", default=0,
                help="Path to video file or integer representing webcam index"
                + " (default 0).")
args = vars(ap.parse_args())
###################################################

frameInfo = FrameInfo()
facePoint = FacePoint()
video_getter = None
video_shower = None
facePointTemp = FacePoint()
currentTime = 0
startTime = datetime.now()


def putIterationsPerSec(frame, iteration_per_sec):
    cv2.putText(frame, '{:0.0f}'.format(iteration_per_sec),
                (10, 450), cv2.FONT_HERSHEY_COMPLEX, 0.6, (255, 255, 255))
    return frame

#FrameInfo(frameWidth=640, frameWidthLimitR=576, frameWidthLimitL=64, frameHeight=480, frameHeightLimitB=432, frameHeightLimitT=48)


def start(source=0):
    global video_getter, video_shower, frameInfo, facePoint, moveDirection, facePointTemp, startTime, currentTime
    isSaving = True
    isFaceDetected = True
    # Get video feed from camera or video file
    video_getter = VideoGet(source).start()
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
        sleep(0.001)
        facePoint = video_shower.facePoint

        # TODO Dont send any command when face goes out of visible screen while it is out of safe area
        currentTime = (datetime.now() - startTime).seconds
        if (currentTime % 2 == 0)  and (currentTime != 0):
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

        if video_getter.stopped or video_shower.stopped or movement.stopped:
            video_shower.stop()
            video_getter.stop()
            movement.stop()
            raspberry.stop()
            break

        frame = video_getter.frame
        frame = putIterationsPerSec(frame, cps.countsPerSec())
        video_shower.frame = frame
        cps.increment()


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
    main()
