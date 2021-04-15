import threading
import numpy as np
from dataClass.FrameInfo import FrameInfo
from dataClass.FacePoint import FacePoint
import cv2
from datetime import datetime
import os
import pickle


class VideoShow:
    """
    Class that continuously shows a frame using a dedicated thread.
    """

    def __init__(self, frame=None, frameInfo=FrameInfo(), classifier=None):
        self.net = cv2.dnn.readNetFromCaffe(
            'videoProcessing{}deploy.prototxt.txt'.format(os.sep), 'videoProcessing{}res10_300x300_ssd_iter_140000.caffemodel'.format(os.sep))
        self.embedder = cv2.dnn.readNetFromTorch(
            'videoProcessing{}openface.nn4.small2.v1.t7'.format(os.sep))

        # load the actual face recognition model along with the label encoder
        self.recognizer = pickle.loads(
            open("{}{}recognizer.pickle".format(classifier, os.sep), "rb").read())
        self.label = pickle.loads(
            open("{}{}label.pickle".format(classifier, os.sep), "rb").read())

        self.facePoint = FacePoint()
        self.frameInfo = frameInfo
        self.frame = frame
        self.stopped = False
        self.newFrame = frame
        self.isFaceDetected = False

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

            goodDetection = []
            for i in range(0, detections.shape[2]):
                if detections[0, 0, i, 2] > 0.5:
                    goodDetection.append(detections[0, 0, i, 3:7])
            
            if len(goodDetection) > 0:
                self.isFaceDetected = True
            else:
                self.isFaceDetected = False

            for i in range(0, len(goodDetection)):
                # extract the confidence (i.e., probability) associated with the
                # prediction
                # compute the (x, y)-coordinates of the bounding box for the
                # object
                box = goodDetection[i] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")
                X = int(startX)
                Y = int(startY)
                W = int(endX - startX)
                H = int(endY - startY)
                CX = int((startX + endX)/2)
                CY = int((startY + endY)/2)

                face = self.frame[startY:endY, startX:endX]
                (fH, fW) = face.shape[:2]

                # ensure the face width and height are sufficiently large
                if fW < 20 or fH < 20:
                    continue

                blob = cv2.dnn.blobFromImage(face, 1.0 / 255,
                                             (96, 96), (0, 0, 0), swapRB=True, crop=False)
                self.embedder.setInput(blob)
                vec = self.embedder.forward()

                # perform classification to recognize the face
                proba = 0.0
                name = ''
                preds = self.recognizer.predict_proba(vec)[0]
                for me in range(len(preds)):
                    if (preds[me] > 0.4) and (self.label.classes_[me] == 'pratik'):
                        proba = preds[me]
                        name = self.label.classes_[me]

                if (proba == 0.0) and (name == ''):
                    j = np.argmax(preds)
                    proba = preds[j]
                    name = self.label.classes_[j]

                text = "{}: {:.2f}%".format(name, proba * 100)

                self.facePoint = FacePoint(X, Y, W, H, CX, CY)
                # draw the bounding box of the face along with the associated
                # probability
                cv2.rectangle(self.frame, (startX, startY),
                              (endX, endY), (0, 0, 255), 2)
                cv2.putText(self.frame, ("{}".format(
                    text)), (startX, startY - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255))
                # X Axis
                cv2.line(self.frame, (int((startX + endX)/2), int((startY+endY)/2)),
                         (0, int((startY+endY)/2)), (0, 0, 255), 2)
                # Y Axis
                cv2.line(self.frame, (int((startX + endX)/2), int((startY+endY)/2)),
                         (int((startX + endX)/2), 0), (0, 0, 255), 2)

                cv2.putText(self.frame, ("X:{} Y:{} W:{} H:{}".format(
                    X, Y, W, H)), (startX, startY-5), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 0, 255))
            goodDetection.clear()
            self.newFrame = self.frame
            # cv2.imshow("Video", self.frame)
            # cv2.imshow("Gray" , gray)

    def stop(self):
        self.stopped = True
