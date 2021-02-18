import argparse
from dataClass.FrameInfo import FrameInfo
from dataClass.FacePoint import FacePoint
import os
import cv2
from time import sleep
from helper.CountsPerSec import CountsPerSec
from videoProcessing.VideoGet import VideoGet
from videoProcessing.GetFace import GetFaceCamera, GetFaceImage, GetFaceImageWithOldModel
from videoProcessing.GetEmbedded import GetEmbedded
from videoProcessing.TrainModel import TrainModel

from datetime import date, datetime
import argparse

# For parsing text in -h flag


class SmartFormatter(argparse.HelpFormatter):

    def _split_lines(self, text, width):
        if text.startswith('R|'):
            return text[2:].splitlines()
        return argparse.HelpFormatter._split_lines(self, text, width)


# Steps to follow
steps = "R|Step 1 \n\
            If you dont have image with single face\n\
            If you have , Go to step 2 \n\
             a. To extract face from camera \n\
                    python main.py -cam true -person 'name_here'\n\
                    python main.py -cam true -person 'name_here' -o 'output folder'\n\
                    -o is optional , by default it is set to folder 'dataset'\n\
             b. To extract face from images \n\
                    python main.py -img true\n\
                    python main.py -img true -i 'input folder' -o 'output folder'\n\
                    -i is optional , by default it is set to folder 'input'\n\
                    -o is optional , by default it is set to folder 'dataset'\n\
        Step 2 \n\
            python main.py -embed true\n\
            python main.py -embed true -o 'location of images'\n\
        Step 3 \n\
           python main.py -tm true -mo 'model output folder'\n\
           -mo is optional . by default it is set to folder 'output' "
###


# Argument parser
ap = argparse.ArgumentParser(add_help=False, formatter_class=SmartFormatter)
ap.add_argument("-h", "--help", action="help", help=steps, )
ap.add_argument("-p", "--person", default='unknown',
                help="Set person name"
                + " (default name 'unknown').")
ap.add_argument("-cam", "--fromCamera", default=False,
                help="Step 1 To extract face using webcamera"
                + " (default False).")
ap.add_argument("-img", "--fromImage", default=False,
                help="Step 1 To extract face using image set"
                + " (default False).")
ap.add_argument("-embed", "--extractEmbedding", default=False,
                help="Step 2 To extract embeddings from face exxtracted"
                + " (default False).")
ap.add_argument("-tm", "--trainModel", default=False,
                help="Step 3 To train mode after extracting embeddings"
                + " (default False).")
ap.add_argument("-o", "--datasetOutput", default="dataset",
                help="Dataset output folder"
                + " (default folder 'dataset').")
ap.add_argument("-i", "--datasetInput",  default="input",
                help="Dataset input folder"
                + " (default folder 'input').")
ap.add_argument("-mo", "--modelOutput", default="output",
                help="Recgonizer model output folder"
                + " (default folder 'output').")
args = vars(ap.parse_args())
###################################################


def putIterationsPerSec(frame, iteration_per_sec):
    cv2.putText(frame, '{:0.0f}'.format(iteration_per_sec),
                (10, 450), cv2.FONT_HERSHEY_COMPLEX, 0.6, (255, 255, 255))
    return frame


def ExtractFaceCamera(source=0):

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

    # To get face from camera
    # Output folder tree  ----> "outputfolder"/"name of person"/[images]
    # python main.py -cam true -person "name_here"
    # python main.py -cam true -person "name_here" -o "output folder"
    # -o is optional , by default it is set to folder "dataset"
    if(bool(args["fromCamera"])):
        if(not os.path.isdir(args["person"])):
            os.makedirs(
                "{}/{}".format(args["datasetOutput"], args["person"]), exist_ok=True)
        print(
            "OUTPUT IMAGES WILL BE STORED INSIDE {}/{}".format(args["datasetOutput"], args["person"]))
        ExtractFaceCamera()

    # To get face from image
    # Input folder tree   -----> "inputfolder"/"name of person"/[images]
    # python main.py -img true
    # python main.py -img true -i "input folder" -o "output folder"
    # -i is optional , by default it is set to folder "input"
    # -o is optional , by default it is set to folder "dataset"

    elif(bool(args["fromImage"])):
        if(os.path.isdir(args["datasetInput"])):
            GetFaceImage(args["datasetInput"],
                         args["datasetOutput"]).start()
            # GetFaceImageWithOldModel(args["datasetInput"],
            #                     args["datasetOutput"]).start()
        else:
            print('Dataset folder does not exists')

    # To get embeddings
    # python main.py -embed true
    # python main.py -embed true -o "location of images"
    elif(bool(args["extractEmbedding"])):
        if(os.path.isdir(args["datasetOutput"])):
            GetEmbedded(args["datasetOutput"]).start()

    # To train model using embedding
    # python main.py -tm true -mo "model output folder"
    # -mo is optional . by default it is set to folder "output"
    elif(bool(args["trainModel"])):
        TrainModel(args["modelOutput"])
    else:
        os.system('python main.py -h')


if __name__ == "__main__":
    main()
