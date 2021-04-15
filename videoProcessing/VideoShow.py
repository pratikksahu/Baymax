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

                self.facePoint = FacePoint(X, Y, W, H, CX, CY)
                # draw the bounding box of the face along with the associated
                # probability
                cv2.rectangle(self.frame, (startX, startY),
                              (endX, endY), (0, 0, 255), 2)
                # X Axis
                cv2.line(self.frame, (int((startX + endX)/2), int((startY+endY)/2)),
                         (0, int((startY+endY)/2)), (0, 0, 255), 2)
                # Y Axis
                cv2.line(self.frame, (int((startX + endX)/2), int((startY+endY)/2)),
                         (int((startX + endX)/2), 0), (0, 0, 255), 2)

                cv2.putText(self.frame, ("X:{} Y:{} W:{} H:{}".format(
                    X, Y, W, H)), (startX, startY-5), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 0, 255))
            # Draw Constraints in every frame irrespective of whether face has been detected or not
            cv2.putText(self.frame, ("Safe Area Line"), (self.frameInfo.frameWidthLimitL,
                                                         self.frameInfo.frameHeightLimitT - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255))
            cv2.rectangle(self.frame, (self.frameInfo.frameWidthLimitL, self.frameInfo.frameHeightLimitT),
                          (self.frameInfo.frameWidthLimitR, self.frameInfo.frameHeightLimitB), (255, 0, 0), 2)
            goodDetection.clear()
            self.newFrame = self.frame
            # cv2.imshow("Video", self.frame)
            # cv2.imshow("Gray" , gray)

    def stop(self):
        self.stopped = True
