from sklearn.preprocessing import LabelEncoder
from sklearn.svm import *
from sklearn.linear_model import *
import argparse
import pickle
import numpy as np
import shutil
import os

class TrainModel:
    def __init__(self , modelOutput):
        # load the face embeddings
        print("Loading face embeddings of the dataset")
        data = pickle.loads(open("embeddings.pickle", "rb").read())
        
        # encode the labels
        print("Encoding image labels")
        le = LabelEncoder()
        labels = le.fit_transform(data["names"])
        # train the model used to accept the 128-d embeddings of the face and
        # then produce the actual face recognition
        os.makedirs(modelOutput,exist_ok=True)
        print("Training the model usng SVM...")
        for i in (range(21,22)):
            print('C = ',i)
            # recognizer = SVC(C=float(i), kernel="poly", probability=True)
            recognizer = SGDClassifier(loss="log", penalty="l1", max_iter=10000)
            recognizer.fit(data["embeddings"], labels)

            os.makedirs('{}{}C{}'.format(modelOutput,os.sep,i+1),exist_ok=True)
            # write the actual face recognition model to disk
            f = open("{}{}C{}{}recognizer.pickle".format(modelOutput,os.sep,i+1,os.sep), "wb")
            f.write(pickle.dumps(recognizer))
            f.close()

            # write the label encoder to disk
            f = open("{}{}C{}{}label.pickle".format(modelOutput,os.sep,i+1,os.sep), "wb")
            f.write(pickle.dumps(le))
            f.close()
