from imutils.video import VideoStream
import time
import cv2
import picamera
import imutils
import argparse
import numpy as np
from collections import deque


from grip2 import GripPipeline
from FilterG2s import FilterG2s
from G2Class import G2Class

class PipelineWrapper:

    def __init__(self,image):
        self.pw_image = image
        self.gp = GripPipeline()
        self.gp.process(self.pw_image)

    #Use the GripPipeline class to get contours
    def getContours(self):
        cnts = self.gp.filter_contours_output
        return cnts


class FilterContours:

    def __init__(self,image):
        self.pw = PipelineWrapper(image)

    def getApprox(self):
        #Make a pipeline so that we can get contours
        cnts = self.pw.getContours()
        #print("Contours")
        #print(cnts)

        #Initilize empty array of arrays of contour points
        approxPts = []

        #Loop through one contour at a time
        for cnt in cnts:
            #I dont know what epsilon does but we need it to process points
            percentArcLength = 0.01
            epsilon = percentArcLength * cv2.arcLength(cnt, True)
            #Find the array of points or the contour
            pts = cv2.approxPolyDP(cnt, epsilon, True)
            approxPts.append(pts)

        #print("approxPts")
        #print(approxPts)
        #print(len(approxPts[0]))
        return cnts, approxPts



def findG2InFrame(frame):

    fc = FilterContours(frame)
    cnts, approx = fc.getApprox()
    sorter = FilterG2s()
    G2ID = 0
    for c in cnts:
        sorter.addG2(c, approx, G2ID, frame)
        G2ID += 1

    g2 = sorter.findTheOneTrueG2()
    #print("getG2FromFrame g2 = ", g2)
    return g2