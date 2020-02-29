import cv2
import numpy as np
import math

class ManyTo1Ball:
    
    def __init__(self, objs):
        #print ("start of class")
        self.candidateBalls = []
        self.theOneTrueBall = None
        self.process(objs)
        
    def process(self, objs):
        #print ("process function begins")
        self.loopOverCntsAndCreateBallObjects(objs)
        self.thereCanBeOnlyOne()
        
    def loopOverCntsAndCreateBallObjects(self, objs):
        #print ("loop and create begins")
        for i in range(0, len(objs)):
            if objs[i].id == 36:
                tempBall = objs[i]
                tempBall.cX = (tempBall.bbox.xmin + tempBall.bbox.xmax)/2
                tempBall.cY = (tempBall.bbox.ymin + tempBall.bbox.ymax)/2
                tempBall.xRadius = (tempBall.bbox.xmin - tempBall.bbox.xmax)/2
                tempBall.yRadius = (tempBall.bbox.ymin + tempBall.bbox.ymax)/2
                tempBall.radius = (xRadius +yRadius)/2
                self.candidateBalls.append(tempBall)
            #print (self.candidateBalls)
                
    def thereCanBeOnlyOne(self):
        #print ("there can be only one begins")
        #if len(self.candidateBalls) == 0:
            #print("no balls")
        if len(self.candidateBalls) > 0:
            maybe = self.candidateBalls[0]
            numCandidateBalls = len(self.candidateBalls)
            for i in range (0, numCandidateBalls):
                if maybe.radius <= self.candidateBalls[i].radius:
                    maybe = self.candidateBalls[i]
            self.theOneTrueBall = maybe

    def calcDistance(self, radius):
        f_x = 705.43687884 #1246.02212 picam v2 #705.43687884 for picam v1 #825
        F_x = f_x*(.14/(2*radius))
        return F_x
    
    def calcAngle(self, cX, size):
        f_x = 705.43687884
        pixelOffset = cX - (size / 2)
        angle = math.degrees(math.atan(pixelOffset/f_x))
        return angle
        
    def coord(self):
        if len(self.candidateBalls) > 0:
            print ("Radius: ", self.theOneTrueBall.radius)
            print ("Center: ", self.theOneTrueBall.centroid)
