import cv2
import imutils
import numpy as np
import argparse
from collections import deque
import sys
import picamera
from imutils.video import VideoStream
import time
import math
import logging
from networktables import NetworkTables
from networktables import NetworkTablesInstance


def main(argv=None):
    index = 0
    ap= argparse.ArgumentParser()
    #ap.add_argument("-v", "--video", help="path to the (optional) video file")
    ap.add_argument("-i", "--input", help="path to the input image file")
    ap.add_argument("-b", "--buffer", type=int, default=64, help="max buffer size")
    ap.add_argument("-p", "--picamera", type=int, default=1, help="whether or not the Raspi camera should be used")
    args = vars(ap.parse_args())

    #---------------
    #  INIT  ...move to proper fxn later
    #----------------
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

    logging.basicConfig(level=logging.DEBUG)



    while True:
        #Grab the frame
        frame = vs.read()

        scale = 1

        cv2.imshow("take_pics", frame)

        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break
        if key == ord("c"):
            outputfilename = str("image_"+str(index)+".jpg")
            cv2.imwrite(outputfilename, frame)
            print("Took pic:", outputfilename)
            index = index + 1

    cv2.destroyAllWindows()
    vs.stop()


if __name__ == "__main__":
    main(sys.argv)

