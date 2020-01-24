
import cv2 as cv
import grip
import imutils
import argparse
import numpy as np
from collections import deque


class PipelineWrapper:

    def __init__(self):
        self.gp = grip

    #Uses the grip class to process the image
    def processImage(self, image):
        #Make an instance of the grip class and process the given image
        self.gp.process(image)

    #Use the grip class to get contours
    def getContours(self):
        cnts = self.gp.filter_contours_output
        return cnts


class FilterContours:

    def __init__(self):
        self.pw = PipelineWrapper()

    def getApprox(self):
        #Make a pipeline so that we can get contours
        cnts = self.pw.getContours()

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

        print(approx)
        #return approx


def VisionProcessing():

    pw = PipelineWrapper()
    fc = FilterContours()

    #Get video and buffer from terminal as well as image p
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--video", help = "path  to the (optional) video file")
    ap.add_argument("-b", "--buffer", type=int, default=64, help="max buffer size")
    args = vars(ap.parse_args())

    #Initilize tracked points array
    pts = deque(maxlen = args["buffer"])

    #Makes sure were getting a camera stream
    if not args.get("video", False):
        camera = cv.VideoCapture(0)
    else:
        camera = cv.VideoCapture(args["video"])

    #THE GIGALOOP
    while True:
        #Grab the frame
        (grabbed, frame) = camera.read()

        #Stop the loop if the camera stops streaming
        if args.get("video") and not grabbed:
            break

        #Resize image and run it through the pipeline
        frame = imutils.resize(frame, width = 1000)

        frame = pw.processImage(frame)
        fc.getApprox()



VisionProcessing()


