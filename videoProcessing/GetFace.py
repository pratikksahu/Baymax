import threading
import numpy as np
from dataClass.FrameInfo import FrameInfo
from dataClass.FacePoint import FacePoint
import cv2
from datetime import datetime
import os
import imutils

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

    def start(self):
        threading.Thread(name='show', target=self.show).start()
        return self

    def show(self):
        while not self.stopped:
            total = 0
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
                    self.facePoint = FacePoint(X, Y, W, H)
                    faceimg = self.frame[(
                        Y - 50):(Y + 20) + H, (X - 40):X + W + 50]
                    cv2.imwrite(
                        "{}{}{}.jpg".format(self._folderName, os.sep, total), faceimg)
                    total = total + 1
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

                        image = cv2.imread("{}{}{}{}{}".format(
                            root, os.sep, dir, os.sep, fileName))
                        image = imutils.resize(image, width=600)
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

                            if confidence > 0.4:
                                print("found")
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

                                # faceimg = image[(
                                #     Y - 20):(Y + 20) + H, (X - 20):X + W + 20]

                                os.makedirs("{}{}{}".format(
                                    self._outputFolder, os.sep, dir), exist_ok=True)
                                cv2.imwrite(
                                    "{}{}{}{}{}.jpg".format(self._outputFolder, os.sep, dir, os.sep, total), faceimg)
                                total = total + 1
