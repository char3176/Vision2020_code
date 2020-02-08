import cv2
import imutils
import numpy as np
import argparse
from collections import deque
import sys
import picamera
from imutils.video import VideoStream
import time

from ballPipeline import BallPipeline
from ballClass import BallClass
from manyTo1B import ManyTo1B
from newBallPipeline import NewBallPipeline

def main(argv=None):
    ap= argparse.ArgumentParser()
    #ap.add_argument("-v", "--video", help="path to the (optional) video file")
    ap.add_argument("-i", "--input", help="path to the input image file")
    ap.add_argument("-b", "--buffer", type=int, default=64, help="max buffer size")
    ap.add_argument("-p", "--picamera", type=int, default=1, help="whether or not the Raspi camera should be used")
    #ap.add_argument("-p", "--picamera", type=int, default=1, help="whether or not the Raspi camera should be used")
    args = vars(ap.parse_args())
#    vs = VideoStream(usePiCamera=args["picamera"] > 0, resolution=(320, 240),framerate=60).start()
#    vs = VideoStream(usePiCamera=args["picamera"] > 0, resolution=(640, 480),framerate=60).start()
    vs = VideoStream(usePiCamera=args["picamera"] > 0, resolution=(640, 480),framerate=90).start()
#    vs = VideoStream(usePiCamera=args["picamera"] > 0, resolution=(1280, 720),framerate=60).start()
#    vs = VideoStream(usePiCamera=args["picamera"] > 0, resolution=(1640, 922),framerate=40).start()
#    vs = VideoStream(usePiCamera=args["picamera"] > 0, resolution=(1920, 1080),framerate=30).start()
#    vs = VideoStream(usePiCamera=args["picamera"] > 0, resolution=(1640, 1232),framerate=40).start()
#    vs = VideoStream(usePiCamera=args["picamera"] > 0, resolution=(3280, 2464),framerate=15).start()
    time.sleep(2.0)
    vs.camera.brightness = 50
    vs.camera.contrast = 0
    vs.camera.saturation = 0

    #DA MASTA LOOP
    while True:
        #Grab the frame
        frame = vs.read()
        #frame = imutils.resize(frame, width=320)
        #frame = imutils.rotate(frame, 90)

        #with picamera.array.PiRGBArray(camera) as stream:
            #camera.capture(stream, format="bgr")
            #frame = stream.array

        #img = np.zeros((600, 600, 3), np.uint8)
        img = frame.copy()
        scale = 1
        bp = BallPipeline()
        cnts = bp.process(img)
        mb = ManyTo1B(cnts)
        #mb.coord()
        if len(mb.candidateBalls) > 0:
            cv2.circle(img, mb.theOneTrueBall.centroid, int (mb.theOneTrueBall.radius), (0, 0, 255), 4)
            cv2.circle(img, mb.theOneTrueBall.centroid, 4, (0, 0, 255), -1)
        cv2.imshow("BallTrack", img)

        #frame = VisionProcessing(frame)
        #cv.imshow("VP", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break

    cv2.destroyAllWindows()
    vs.stop()


if __name__ == "__main__":
    main(sys.argv)
'''
img = cv2.imread("ball2.jpg")
bp = BallPipeline()
#bp = NewBallPipeline()
cnts = bp.process(img)
mb = ManyTo1B(cnts)
mb.coord()
'''

