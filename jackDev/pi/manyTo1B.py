import cv2
import numpy as np
import math

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

    def calcDistance(self, radius):
        f_x = 1246.02212 #divide by approximately 2 gives approx correct distance if D is between 0 and 2 m
        F_x = f_x*(.14/(2*radius)) #mm
        #m_F_x = F_x / 1000 #m
        return F_x
        
    def coord(self):
        if len(self.candidateBalls) > 0:
            print ("Radius: ", self.theOneTrueBall.radius)
            print ("Center: ", self.theOneTrueBall.centroid)
