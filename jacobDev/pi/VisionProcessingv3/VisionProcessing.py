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



ap = argparse.ArgumentParser()
ap.add_argument("-p", "--picamera", type=int, default=1, help="whether or not the Raspi camera should be used")
args = vars(ap.parse_args())

#vs = VideoStream(usePiCamera=args["picamera"] > 0, resolution=(320, 240),framerate=60).start()
vs = VideoStream(usePiCamera=args["picamera"] > 0, resolution=(640, 480),framerate=60).start()
#vs = VideoStream(usePiCamera=args["picamera"] > 0, resolution=(640, 480),framerate=90).start()
#vs = VideoStream(usePiCamera=args["picamera"] > 0, resolution=(1280, 720),framerate=60).start()
#vs = VideoStream(usePiCamera=args["picamera"] > 0, resolution=(1640, 922),framerate=40).start()
#vs = VideoStream(usePiCamera=args["picamera"] > 0, resolution=(1920, 1080),framerate=30).start()
#vs = VideoStream(usePiCamera=args["picamera"] > 0, resolution=(1640, 1232),framerate=40).start()
#vs = VideoStream(usePiCamera=args["picamera"] > 0, resolution=(3280, 2464),framerate=15).start()

time.sleep(2.0)
vs.camera.brightness = 30
vs.camera.contrast = 100
vs.camera.saturation = 100

#DA MASTA LOOP
while True:
        #Grab the frame
        frame = vs.read()
        #frame = imutils.resize(frame, width=320)
        #frame = imutils.rotate(frame, 90)

        #with picamera.array.PiRGBArray(camera) as stream:
            #camera.capture(stream, format="bgr")
            #frame = stream.array

        g2 = findG2InFrame(frame)
        if g2 is not None:
          frame = g2.drawFittingOnFrame(frame)

        #frame = VisionProcessing(frame)
        cv2.imshow("VP", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            cv2.imwrite("white.jpg", frame)
            break

cv2.destroyAllWindows()
vs.stop()
