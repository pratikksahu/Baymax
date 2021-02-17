import numpy as np
import argparse
import imutils
import pickle
import cv2
import os

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
                help="path to input image")
args = vars(ap.parse_args())

print("[INFO] loading face detector...")
detector = cv2.dnn.readNetFromCaffe(
    'videoProcessing{}deploy.prototxt.txt'.format(os.sep), 'videoProcessing{}res10_300x300_ssd_iter_140000.caffemodel'.format(os.sep))
# load our serialized face embedding model from disk
print("[INFO] loading face recognizer...")
embedder = cv2.dnn.readNetFromTorch(
    'videoProcessing{}openface.nn4.small2.v1.t7'.format(os.sep))
# load the actual face recognition model along with the label encoder
recognizer = pickle.loads(
    open("output{}recognizer.pickle".format(os.sep), "rb").read())
le = pickle.loads(
    open("output{}label.pickle".format(os.sep), "rb").read())

image = cv2.imread(args["image"])
image = imutils.resize(image, width=1080)
(h, w) = image.shape[:2]
# construct a blob from the image
imageBlob = cv2.dnn.blobFromImage(
    cv2.resize(image, (300, 300)), 1.0, (300, 300),
    (104.0, 177.0, 123.0), swapRB=False, crop=False)
# apply OpenCV's deep learning-based face detector to localize
# faces in the input image
detector.setInput(imageBlob)
detections = detector.forward()

for i in range(0, detections.shape[2]):
    # extract the confidence (i.e., probability) associated with the
    # prediction
    confidence = detections[0, 0, i, 2]
    # filter out weak detections
    if confidence > 0.5:
        # compute the (x, y)-coordinates of the bounding box for the
        # face
        box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
        (startX, startY, endX, endY) = box.astype("int")
        # extract the face ROI
        face = image[startY:endY, startX:endX]
        (fH, fW) = face.shape[:2]
        # ensure the face width and height are sufficiently large
        if fW < 20 or fH < 20:
            continue
        faceBlob = cv2.dnn.blobFromImage(face, 1.0 / 255, (96, 96),
                                         (0, 0, 0), swapRB=True, crop=False)
        embedder.setInput(faceBlob)
        vec = embedder.forward()
        # perform classification to recognize the face
        preds = recognizer.predict_proba(vec)[0]
        j = np.argmax(preds)
        proba = preds[j]
        name = le.classes_[j]
        text = "{}: {:.2f}%".format(name, proba * 100)
        y = startY - 10 if startY - 10 > 10 else startY + 10
        cv2.rectangle(image, (startX, startY), (endX, endY),
                      (0, 0, 255), 2)
        cv2.putText(image, text, (startX, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
# show the output image
cv2.imshow("Image", image)
cv2.waitKey(0)
