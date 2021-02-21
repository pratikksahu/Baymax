from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
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
        os.makedirs('classifier',exist_ok=True)
        print("Training the model usng SVM...")
        for i in (range(4,10)):
            recognizer = SVC(C=float(i), kernel="poly", probability=True)
            recognizer.fit(data["embeddings"], labels)

            if(os.path.isdir(modelOutput)):
                shutil.rmtree(modelOutput)
            os.makedirs('classifier{}{}_C{}'.format(os.sep,modelOutput,i+1),exist_ok=True)
            # write the actual face recognition model to disk
            f = open("classifier{}{}_C{}{}recognizer.pickle".format(os.sep,modelOutput,i+1,os.sep), "wb")
            f.write(pickle.dumps(recognizer))
            f.close()

            # write the label encoder to disk
            f = open("classifier{}{}_C{}{}label.pickle".format(os.sep,modelOutput,i+1,os.sep), "wb")
            f.write(pickle.dumps(le))
            f.close()
