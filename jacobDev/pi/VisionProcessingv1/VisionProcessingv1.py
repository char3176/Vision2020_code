
import cv2 as cv
import imutils
import argparse
import numpy as np
from collections import deque


from grip import GripPipeline
from FilterG2s import FilterG2s


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
            epsilon = percentArcLength * cv.arcLength(cnt, True)
            #Find the array of points or the contour
            pts = cv.approxPolyDP(cnt, epsilon, True)
            approxPts.append(pts)

        #print("approxPts")
        #print(approxPts)
        #print(len(approxPts[0]))
        return cnts, approxPts



def VisionProcessing(image):

    fc = FilterContours(image)
    cnts, approx = fc.getApprox()
    sorter = FilterG2s()
    approxID = 0
    for c in cnts:
        sorter.addG2(c, approx, approxID)
        approxID += approxID

    g2 = sorter.findTheG2()

    #Get video and buffer from terminal as well as image p
#    ap = argparse.ArgumentParser()
#    ap.add_argument("-v", "--video", help = "path  to the (optional) video file")
#    ap.add_argument("-b", "--buffer", type=int, default=64, help="max buffer size")
#    args = vars(ap.parse_args())

    #Initilize tracked points array
#    pts = deque(maxlen = args["buffer"])

    #Makes sure were getting a camera stream
#    if not args.get("video", False):
#        camera = cv.VideoCapture(0)
#    else:
#        camera = cv.VideoCapture(args["video"])

    #DA MASTA LOOP
#    while True:
        #Grab the frame
#        (grabbed, frame) = camera.read()

        #Stop the loop if the camera stops streaming
#        if args.get("video") and not grabbed:
#            break

        #Resize image and run it through the pipeline
#        frame = imutils.resize(frame, width = 1000)

#        frame = pw.processImage(frame)
#        fc.getApprox()



image = cv.imread("BlueGoal-180in-Center.jpg")
VisionProcessing(image)


