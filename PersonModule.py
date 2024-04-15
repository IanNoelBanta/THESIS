import math
import cv2
import torch
import numpy as np
import json
import AmpalayaModule


class PersonDetector:
    def __init__(self, model, maxPerson=1):
        # self.model = torch.hub.load("ultralytics/yolov5", "custom", path="D:/repos/THESIS/best.pt",force_reload=True)
        self.model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
        self.maxPerson = maxPerson
        self.search = None
        self.list_of_object = []
        self.currentId = 0

    def findPerson(self, img, draw=True, flipType=True):
        self.results = self.model(img)
        json_data = self.results.pandas().xyxy[0].to_json(orient="records")
        data = json.loads(json_data)

        for obj in data:
            if obj["name"] == "bottle" and obj["name"] not in self.list_of_object:
                ampalaya = AmpalayaModule.Ampalaya(self.currentId)

        if draw:
            img = np.squeeze(self.results.render())

        return self.list_of_object, img
    
    def startDetection(self):
        self.search = True

    def stopDetection(self):
        self.search = False