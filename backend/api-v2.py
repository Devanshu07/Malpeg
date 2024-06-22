import feature_extractor as fe
import os
import pickle
from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
from flask import request, Response
import numpy as np
import json
import PIL.Image as Image
import io
import base64
from struct import unpack
import pandas as pd
import sys
import glob
import pickle

app = Flask(__name__)
CORS(app)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument("image")

class Predict(Resource):
    def post(self):
        args = parser.parse_args()
        decodeit = open('image', 'wb')
        decodeit.write(base64.b64decode(bytes(args["image"], 'utf-8')))
        decodeit.close()
        fe.extract_features()
        model = pickle.load(open("./xgboost.pkl", 'rb'))
        test = pd.read_csv('test.csv',header=None)
        x_test = np.array(test.iloc[1:, 1:10])  
        y_test = np.array(test.iloc[1:, 11])  
        res = model.predict(x_test)
        print(res)
        class_ = ""
        if res == 0:
            class_ = "benign"
        else:
            class_ = "malicious"
        return {"class": class_}

api.add_resource(Predict, "/predict")

if __name__ == "__main__":
    app.run(debug=True)