import threading
import numpy as np
from dataClass.FrameInfo import FrameInfo
from dataClass.FacePoint import FacePoint
import cv2
from datetime import datetime
import os
import imutils
import pickle

class GetFaceCamera:
    """
    Class that continuously shows a frame using a dedicated thread.
    """

    def __init__(self, folderName, frame=None):
        self.net = cv2.dnn.readNetFromCaffe(
            'videoProcessing{}deploy.prototxt.txt'.format(os.sep), 'videoProcessing{}res10_300x300_ssd_iter_140000.caffemodel'.format(os.sep))
        self.frame = frame
        self._folderName = folderName
        self.stopped = False
        self._total = 0

    def start(self):
        threading.Thread(name='show', target=self.show).start()
        return self

    def show(self):
        while not self.stopped:

            (h, w) = self.frame.shape[:2]
            blob = cv2.dnn.blobFromImage(
                self.frame, 1.0, (300, 300), (104.0, 177.0, 123.0))
            self.net.setInput(blob)
            detections = self.net.forward()
            for i in range(0, detections.shape[2]):
                # extract the confidence (i.e., probability) associated with the
                # prediction
                confidence = detections[0, 0, i, 2]

                # filter out weak detections by ensuring the `confidence` is
                # greater than the minimum confidence

                if confidence > 0.3:
                    # compute the (x, y)-coordinates of the bounding box for the
                    # object
                    box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                    (startX, startY, endX, endY) = box.astype("int")
                    X = int(startX)
                    Y = int(startY)
                    W = int(endX - startX)
                    H = int(endY - startY)
                    faceimg = self.frame[(
                        Y - 50):(Y + 20) + H, (X - 40):X + W + 50]
                    cv2.imwrite(
                        "{}{}{}.jpg".format(self._folderName, os.sep, self._total), faceimg)
                    self._total = self._total + 1
            cv2.imshow("Video", self.frame)
            # cv2.imshow("Gray" , gray)
            if cv2.waitKey(1) == ord("q"):
                self.stopped = True

    def stop(self):
        self.stopped = True


class GetFaceImage:
    """
    Class that continuously shows a frame using a dedicated thread.
    """

    def __init__(self, inputFolder, outputFolder):
        self.net = cv2.dnn.readNetFromCaffe(
            'videoProcessing{}deploy.prototxt.txt'.format(os.sep), 'videoProcessing{}res10_300x300_ssd_iter_140000.caffemodel'.format(os.sep))
        self._inputFolder = inputFolder
        self._outputFolder = outputFolder
        self._error = 0

    def start(self):
        threading.Thread(name='show', target=self.show).start()
        return self

    def show(self):
        for root, dirs, files in os.walk(self._inputFolder):
            total = 0
            for dir in dirs:
                if not os.listdir("{}{}{}".format(root, os.sep, dir)):
                    print("Empty Directory {}".format(dir))
                else:
                    path, dirs, files = next(
                        os.walk("{}{}{}".format(root, os.sep, dir)))
                    file_count = len(files)
                    print("Total files in directory {} is {}".format(
                        dir, file_count))
                    for fileName in files:
                        # print(fileName)
                        image = cv2.imread("{}{}{}{}{}".format(
                            root, os.sep, dir, os.sep, fileName))
                        height, width, channels = image.shape

                        if height > width:
                            image = imutils.resize(image, height=int(height * .4), inter=cv2.INTER_AREA)
                        else:
                            image = imutils.resize(image, width=int(width * .8) , inter=cv2.INTER_AREA)

                        (h, w) = image.shape[:2]
                        blob = cv2.dnn.blobFromImage(
                            cv2.resize(image, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))
                        self.net.setInput(blob)
                        detections = self.net.forward()
                        for i in range(0, detections.shape[2]):
                            # extract the confidence (i.e., probability) associated with the
                            # prediction
                            confidence = detections[0, 0, i, 2]

                            # filter out weak detections by ensuring the `confidence` is
                            # greater than the minimum confidence

                            if confidence > 0.8:
                                # compute the (x, y)-coordinates of the bounding box for the
                                # object
                                box = detections[0, 0, i, 3:7] * \
                                    np.array([w, h, w, h])
                                (startX, startY, endX, endY) = box.astype("int")
                                X = int(startX)
                                Y = int(startY)
                                W = int(endX - startX)
                                H = int(endY - startY)
                                faceimg = image[Y:Y + H, X:X + W]

                                os.makedirs("{}{}{}".format(
                                    self._outputFolder, os.sep, dir), exist_ok=True)
                                try:
                                    cv2.imwrite(
                                        "{}{}{}{}{}.jpg".format(self._outputFolder, os.sep, dir, os.sep, total), faceimg)
                                except:
                                    print("Error in file {} . Remove the image".format(fileName))
                                total = total + 1


class GetFaceImageWithOldModel:
    """
    Class that continuously shows a frame using a dedicated thread.
    """

    def __init__(self, inputFolder, outputFolder):
        self.net = cv2.dnn.readNetFromCaffe(
            'videoProcessing{}deploy.prototxt.txt'.format(os.sep), 'videoProcessing{}res10_300x300_ssd_iter_140000.caffemodel'.format(os.sep))
        self.embedder = cv2.dnn.readNetFromTorch(
            'videoProcessing{}openface.nn4.small2.v1.t7'.format(os.sep))

        # load the actual face recognition model along with the label encoder
        self.recognizer = pickle.loads(
            open("output{}recognizer.pickle".format(os.sep), "rb").read())
        self.label = pickle.loads(
            open("output{}label.pickle".format(os.sep), "rb").read())

        self._inputFolder = inputFolder
        self._outputFolder = outputFolder
        self._error = 0

    def start(self):
        threading.Thread(name='show', target=self.show).start()
        return self

    def show(self):
        for root, dirs, files in os.walk(self._inputFolder):
            total = 0
            for dir in dirs:
                if not os.listdir("{}{}{}".format(root, os.sep, dir)):
                    print("Empty Directory {}".format(dir))
                else:
                    path, dirs, files = next(
                        os.walk("{}{}{}".format(root, os.sep, dir)))
                    file_count = len(files)
                    print("Total files in directory {} is {}".format(
                        dir, file_count))
                    for fileName in files:
                        # print(fileName)
                        image = cv2.imread("{}{}{}{}{}".format(
                            root, os.sep, dir, os.sep, fileName))
                        height, width, channels = image.shape

                        if height > width:
                            image = imutils.resize(image, height=int(height * .4), inter=cv2.INTER_AREA)
                        else:
                            image = imutils.resize(image, width=int(width * .8) , inter=cv2.INTER_AREA)

                        (h, w) = image.shape[:2]
                        blob = cv2.dnn.blobFromImage(
                            cv2.resize(image, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))
                        self.net.setInput(blob)
                        detections = self.net.forward()
                        for i in range(0, detections.shape[2]):
                            # extract the confidence (i.e., probability) associated with the
                            # prediction
                            confidence = detections[0, 0, i, 2]

                            # filter out weak detections by ensuring the `confidence` is
                            # greater than the minimum confidence

                            if confidence > 0.7:
                                # compute the (x, y)-coordinates of the bounding box for the
                                # object
                                box = detections[0, 0, i, 3:7] * \
                                    np.array([w, h, w, h])
                                (startX, startY, endX, endY) = box.astype("int")
                                X = int(startX)
                                Y = int(startY)
                                W = int(endX - startX)
                                H = int(endY - startY)
                                face = image[startY:endY, startX:endX]
                                (fH, fW) = face.shape[:2]

                                # ensure the face width and height are sufficiently large
                                if fW < 20 or fH < 20:
                                    continue
                                
                                blob = cv2.dnn.blobFromImage(face, 1.0 / 255,
                                                                 (96, 96), (0, 0, 0), swapRB=True, crop=False)
                                self.embedder.setInput(blob)
                                vec = self.embedder.forward()

                                # perform classification to recognize the face
                                preds = self.recognizer.predict_proba(vec)[0]            
                                j = np.argmax(preds)
                                proba = preds[j]
                                name = self.label.classes_[j]

                                os.makedirs("{}{}{}".format(
                                    self._outputFolder, os.sep, dir), exist_ok=True)
                                try:
                                    if(proba > 0.7) and (name == 'pratik'):
                                        cv2.imwrite(
                                            "{}{}{}{}{}.jpg".format(self._outputFolder, os.sep, dir, os.sep, total), image)
                                        total = total + 1
                                except:
                                    print("Error in file {} . Remove the image".format(fileName))
