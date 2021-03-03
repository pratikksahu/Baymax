import threading
import numpy as np
from dataClass.FrameInfo import FrameInfo
from dataClass.FacePoint import FacePoint
import cv2
from datetime import datetime
import os
import pickle
import imutils


class GetEmbedded:
    """
    Class that continuously shows a frame using a dedicated thread.
    """

    def __init__(self, datasetFolder):
        self.net = cv2.dnn.readNetFromCaffe(
            'videoProcessing{}deploy.prototxt.txt'.format(os.sep), 'videoProcessing{}res10_300x300_ssd_iter_140000.caffemodel'.format(os.sep))
        self.embedder = cv2.dnn.readNetFromTorch(
            'videoProcessing{}openface.nn4.small2.v1.t7'.format(os.sep))
        self._datasetFolder = datasetFolder
        self.stopped = False
        self.knownNames = []
        self.knownEmbeddings = []

    def start(self):
        threading.Thread(name='show', target=self.show).start()
        return self

    def show(self):
        t = 0
        name = ''
        for root, dirs, files in os.walk(self._datasetFolder):
            for dir in dirs:
                if not os.listdir("{}{}{}".format(root, os.sep, dir)):
                    print("Empty Directory {}".format(dir))
                else:
                    path, dirs, files = next(
                        os.walk("{}{}{}".format(root, os.sep, dir)))
                    file_count = len(files)
                    print("Total files in directory {} is {}".format(
                        dir, file_count))
                    if(dir == 'pratik') or (dir == 'indian'):
                        name = dir
                        print('T RESET')
                        t = 0
                    else:
                        name = 'unknown'
                    if(dir == '00000') or (dir == 'pratik') or (dir == 'indian'):
                        for fileName in files:
                            if(dir == '00000') and t == 400:
                                t = 0
                                break
                                
                            image_color = cv2.imread("{}{}{}{}{}".format(
                                root, os.sep, dir, os.sep, fileName))
                            image = cv2.cvtColor(image_color, cv2.COLOR_BGR2GRAY)                                                        
                            height, width, channels = image.shape

                            if height > width:
                                image = imutils.resize(image, height=int(height * .4), inter=cv2.INTER_AREA)
                            else:
                                image = imutils.resize(image, width=int(width * .8) , inter=cv2.INTER_AREA)

                            (h, w) = image.shape[:2]
                            blob = cv2.dnn.blobFromImage(
                            cv2.resize(image, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0) , swapRB=False , crop=False)
                            self.net.setInput(blob)
                            detections = self.net.forward()

                            if len(detections) > 0:
                                # Assuming that each image has only ONE
                                # face, so find the bounding box with the largest probability
                                i = np.argmax(detections[0, 0, :, 2])
                                confidence = detections[0, 0, i, 2]

                                # ensure that the detection with the 50% probabilty thus helping filter out weak detections
                                if confidence > 0.8:
                                    # compute the (x, y)-coordinates of the bounding box for
                                    # the face
                                    box = detections[0, 0, i, 3:7] * \
                                        np.array([w, h, w, h])
                                    (startX, startY, endX, endY) = box.astype("int")

                                    # extract the face ROI and grab the ROI dimensions
                                    face = image[startY:endY, startX:endX]
                                    (fH, fW) = face.shape[:2]

                                    # ensure the face width and height are sufficiently large
                                    if fW < 20 or fH < 20:
                                        continue

                                    # construct a blob for the face ROI, then pass the blob
                                    # through our face embedding model to obtain the 128-d
                                    # quantification of the face
                                    faceBlob = cv2.dnn.blobFromImage(face, 1.0 / 255,
                                                                     (96, 96), (0, 0, 0), swapRB=True, crop=False)
                                    self.embedder.setInput(faceBlob)
                                    vec = self.embedder.forward()

                                    # add the name of the person + corresponding face
                                    # embedding to their respective lists
                                    self.knownNames.append(name)
                                    self.knownEmbeddings.append(vec.flatten())
                                    if t % 100 == 0:
                                        print("{} images processed".format(t))
                                    t = t+1
        if len(self.knownEmbeddings) > 0 and len(self.knownNames) > 0:
            data = {"embeddings": self.knownEmbeddings,
                    "names": self.knownNames}
            f = open("embeddings.pickle", "wb")
            f.write(pickle.dumps(data))
            f.close()
