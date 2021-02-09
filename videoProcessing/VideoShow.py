import threading
import numpy as np
from dataClass.FrameInfo import FrameInfo
from dataClass.FacePoint import FacePoint
import cv2


class VideoShow:
    """
    Class that continuously shows a frame using a dedicated thread.
    """

    def __init__(self, frame=None, frameInfo=FrameInfo()):
        self.net = cv2.dnn.readNetFromCaffe(
            'videoProcessing/deploy.prototxt.txt', 'videoProcessing/res10_300x300_ssd_iter_140000.caffemodel')
        self.facePoint = FacePoint()
        self.frameInfo = frameInfo
        self.frame = frame
        self.stopped = False

    def start(self):
        threading.Thread(name='show', target=self.show).start()
        return self

    def show(self):
        while not self.stopped:
            (h, w) = self.frame.shape[:2]
            blob = cv2.dnn.blobFromImage(self.frame, 1.0, (300, 300), (104.0, 177.0, 123.0))
            # blob = cv2.dnn.blobFromImage(cv2.resize(
                # self.frame, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))
            self.net.setInput(blob)
            detections = self.net.forward()

            for i in range(0, detections.shape[2]):
                # extract the confidence (i.e., probability) associated with the
                # prediction
                confidence = detections[0, 0, i, 2]

                # filter out weak detections by ensuring the `confidence` is
                # greater than the minimum confidence

                if confidence < 0.4:
                    continue
                    
                # compute the (x, y)-coordinates of the bounding box for the
                # object
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")
                X = int(startX/2)
                Y = int(startY/2)
                W = int(endX/2)
                H = int(endY/2)
                self.facePoint = FacePoint(startX, startY, endX, endY)
                # draw the bounding box of the face along with the associated
                # probability
                cv2.rectangle(self.frame, (startX, startY),
                              (endX, endY), (0, 0, 255), 2)
                cv2.putText(self.frame ,("X:{} Y:{} W:{} H:{}".format(startX, startY, endX, endY)) , (startX, startY-5) , cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 0, 255) )                              
            # Draw Constraints in every frame irrespective of whether face has been detected or not
            cv2.putText(self.frame, ("Safe Area Line"), (self.frameInfo.frameWidthLimitL,
                                                         self.frameInfo.frameHeightLimitT - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255))
            cv2.rectangle(self.frame, (self.frameInfo.frameWidthLimitL, self.frameInfo.frameHeightLimitT),
                          (self.frameInfo.frameWidthLimitR, self.frameInfo.frameHeightLimitB), (255, 0, 0), 2)

            cv2.imshow("Video", self.frame)
            # cv2.imshow("Gray" , gray)
            if cv2.waitKey(1) == ord("q"):
                self.stopped = True

    def stop(self):
        self.stopped = True
