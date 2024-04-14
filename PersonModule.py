import math
import cv2
import torch
import numpy as np
import json


class PersonDetector:
    def __init__(self, model, maxPerson=1):
        self.model = torch.hub.load("ultralytics/yolov5", "yolov5s")
        self.maxPerson = maxPerson
        self.search = None

    def findPerson(self, img, draw=True, flipType=True):
        # self.results = self.model(img)
        # json_data = self.results.pandas().xyxy[0].to_json(orient="records")
        # data = json.loads(json_data)
        # names = [obj["name"] for obj in data]

        if self.search:
            response = "DETECTING"
        else:
            response = "NOT DETECTING"

        # if "person" in names:
        #     self.search = False


        # print(self.results.xyxy[0])

        if draw:
            img = cv2.putText(img, response, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        
        return response, img
    
    def startDetection(self):
        self.search = True

    def stopDetection(self):
        self.search = False