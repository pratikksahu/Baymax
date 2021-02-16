import argparse
from dataClass.FrameInfo import FrameInfo
from dataClass.FacePoint import FacePoint
import os
import cv2
from time import sleep
from helper.CountsPerSec import CountsPerSec
from videoProcessing.VideoGet import VideoGet
from videoProcessing.GetFace import GetFaceCamera, GetFaceImage
from videoProcessing.GetEmbedded import GetEmbedded
from videoProcessing.TrainModel import TrainModel

from datetime import date, datetime

# Argument parser
ap = argparse.ArgumentParser()
ap.add_argument("--person", "-p", default='unknown',
                help="Debug mode"
                + " (default ExtractedFace).")
ap.add_argument("--fromCamera", "-fcam", default=False,
                help="Step 1 To extract face using webcamera"
                + " (default False).")
ap.add_argument("--fromImage", "-fimg", default=False,
                help="Step 1 To extract face using image set"
                + " (default False).")
ap.add_argument("--extractEmbedding", "-eem", default=False,
                help="Step 2 To extract embeddings from face exxtracted"
                + " (default False).")
ap.add_argument("--trainModel", "-tm", default=False,
                help="Step 3 To train mode after extracting embeddings"
                + " (default False).")
ap.add_argument("--datasetOutput", "-o", default="dataset",
                help="Dataset output folder"
                + " (default dataset).")
ap.add_argument("--datasetInput", "-i", default="input",
                help="Dataset input folder"
                + " (default input).")
args = vars(ap.parse_args())
###################################################

video_getter = None
get_face = None


def putIterationsPerSec(frame, iteration_per_sec):
    cv2.putText(frame, '{:0.0f}'.format(iteration_per_sec),
                (10, 450), cv2.FONT_HERSHEY_COMPLEX, 0.6, (255, 255, 255))
    return frame


def ExtractFaceCamera(source=0):

    global video_getter, get_face

    # Get video feed from camera or video file
    video_getter = VideoGet(source).start()
    # Show processed video frame
    get_face = GetFaceCamera(
        "{}/{}".format(args["datasetOutput"], args["person"]), video_getter.frame).start()

    # FPS Counter
    cps = CountsPerSec().start()

    while True:
        sleep(0.01)

        if video_getter.stopped or get_face.stopped:
            get_face.stop()
            video_getter.stop()
            break

        frame = video_getter.frame
        frame = putIterationsPerSec(frame, cps.countsPerSec())
        get_face.frame = frame
        cps.increment()


def main():

    if(bool(args["fromCamera"])):
        if(not os.path.isdir(args["person"])):
            os.makedirs(
                "{}/{}".format(args["datasetOutput"], args["person"]), exist_ok=True)
        print(
            "OUTPUT IMAGES WILL BE STORED INSIDE {}/{}".format(args["datasetOutput"], args["person"]))
        ExtractFaceCamera()

    if(bool(args["fromImage"])):
        if(os.path.isdir(args["datasetInput"])):
            print(
                "OUTPUT IMAGES WILL BE STORED INSIDE {}".format(args["datasetOutput"]))
            GetFaceImage(args["datasetInput"],
                         args["datasetOutput"]).start()
        else:
            print('Dataset folder does not exists')

    if(bool(args["extractEmbedding"])):
        if(os.path.isdir(args["datasetOutput"])):
            GetEmbedded(args["datasetOutput"]).start()

    if(bool(args["trainModel"])):
        TrainModel("output")


if __name__ == "__main__":
    main()
