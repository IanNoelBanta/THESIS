import math
import cv2
import torch
import numpy as np
import json


class Ampalaya:
    def __init__(self, _id, xmin, ymin, xmax, ymax, confidence, name):
        self.id = _id
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax
        self.confidence = confidence
        self.name = name
    
    def setCoordinates(self, xmin, ymin, xmax, ymax):
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax