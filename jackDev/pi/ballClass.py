import cv2 
import numpy as np

class BallClass:

    def __init__(self, cnt):
        self.centroid = []
        self.cX = 0
        self.cY = 0
        self.rwRadius = 3.5
        self.radius = 0
        self.rwRange = 0
        self.amIBigEnough = False
        self.process(cnt)

    def process(self, cnt):
        self.getCentroid(cnt)
        
    def getCentroid(self, cnt):
        #print(self.cX, self.cY, self.radius)
        ((self.cX,self.cY), self.radius) = cv2.minEnclosingCircle(cnt)
        #print(self.cX, self.cY, self.radius)
        M = cv2.moments(cnt)
        #print(M)
        self.centroid = (int(M["m10"]/M["m00"]), int(M["m01"]/M["m00"]))

    def checkIfBigEnough(self):
        if self.radius > 20:
            self.amIBigEnough = True
            return True
        
    def calcDistance(self, radius):
        diameter = 2 * radius
        dist = math.sqrt(2 * (diameter * diameter))
        return dist
