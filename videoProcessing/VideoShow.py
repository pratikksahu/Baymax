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
        self.newFrame = frame
        self.stopped = False
        self.confidence = 0.0

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
                self.confidence = detections[0, 0, i, 2]

                # filter out weak detections by ensuring the `confidence` is
                # greater than the minimum confidence

                if self.confidence > 0.5:
                    
                    # compute the (x, y)-coordinates of the bounding box for the
                    # object
                    box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                    (startX, startY, endX, endY) = box.astype("int")
                    X = int(startX)
                    Y = int(startY)
                    W = int(endX - startX)
                    H = int(endY - startY)

                    face = self.frame[startY:endY, startX:endX]
                    (fH, fW) = face.shape[:2]

                    # ensure the face width and height are sufficiently large
                    if fW < 20 or fH < 20:
                        continue


                    self.facePoint = FacePoint(X, Y, W, H)                    
                    # draw the bounding box of the face along with the associated
                    # probability
                    cv2.rectangle(self.frame, (startX, startY),
                                  (endX, endY), (0, 0, 255), 2)
                    # cv2.putText(self.frame, ("{}".format(
                    #     text)), (startX, startY - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255))
                    cv2.putText(self.frame, ("X:{} Y:{} W:{} H:{}".format(
                        X, Y, W, H)), (startX, startY-5), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 0, 255))          
            # Draw Constraints in every frame irrespective of whether face has been detected or not
            cv2.putText(self.frame, ("Safe Area Line"), (self.frameInfo.frameWidthLimitL,
                                                         self.frameInfo.frameHeightLimitT - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255))
            cv2.rectangle(self.frame, (self.frameInfo.frameWidthLimitL, self.frameInfo.frameHeightLimitT),
                          (self.frameInfo.frameWidthLimitR, self.frameInfo.frameHeightLimitB), (255, 0, 0), 2)     
            # self.newFrame = self.frame   
            # cv2.imshow("Video", self.frame)
            # cv2.imshow("Gray" , gray)

    def stop(self):
        self.stopped = True
