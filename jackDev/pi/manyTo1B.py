import cv2
import numpy as np

from ballClass import BallClass

class ManyTo1B:
    
    def __init__(self, cnts):
        #print ("start of class")
        self.candidateBalls = []
        self.theOneTrueBall = None
        #print (cnts)
        self.process(cnts)
        

    def process(self, cnts):
        #print ("process function begins")
        self.loopOverCntsAndCreateBallObjects(cnts)
        self.thereCanBeOnlyOne()
        
        
    
    def loopOverCntsAndCreateBallObjects(self, cnts):
        #print ("loop and create begins")
        for i in range(0, len(cnts)):
            tempBall = BallClass(cnts[i])
            #print (tempBall)
            #print (tempBall.cX, tempBall.cY, tempBall.radius, tempBall.amIBigEnough)
            if tempBall.checkIfBigEnough():
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

    def calcDistance(self, theOneTrueBall):
        diameter = 2 * self.theOneTrueBall.radius
        dist = math.sqrt(2 * (diameter * diameter))
        return dist

    def coord(self):
        if len(self.candidateBalls) > 0:
            print ("Radius: ", self.theOneTrueBall.radius)
            print ("Center: ", self.theOneTrueBall.centroid)
