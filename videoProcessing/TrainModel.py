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
        print("Training the model usng SVM...")
        recognizer = SVC(C=2.0, kernel="poly", probability=True)
        recognizer.fit(data["embeddings"], labels)
        
        if(os.path.isdir(modelOutput)):
            shutil.rmtree(modelOutput)
        os.makedirs(modelOutput,exist_ok=True)
        # write the actual face recognition model to disk
        f = open("{}{}recognizer.pickle".format(modelOutput,os.sep), "wb")
        f.write(pickle.dumps(recognizer))
        f.close()

        # write the label encoder to disk
        f = open("{}{}label.pickle".format(modelOutput,os.sep), "wb")
        f.write(pickle.dumps(le))
        f.close()
