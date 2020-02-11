#GENERAL IMPORTS
import cv2
import cv2 as cv
import numpy
import numpy as np
import math
from enum import Enum
import imutils
import argparse
import sys
import picamera
from imutils.video import VideoStream
import time
import logging

#from ballClass.py - moved to general
#from ballPipeline.py - moved to general
#from manyTo1B.py - 1 specific class
#from masterBallClass.py - 4 specific classes
#from newBallPipeline.py - moved to general
#from Crosshair.py - moved to general

logging.basicConfig(
    filename="vision.log",
    level=logging.DEBUG,
    format="%(asctime)s:%(levelname)s:%(messages)s"
    )

def loadCameraConfig():


def visionInit():
    #vs = VideoStream(usePiCamera=args["picamera"] > 0, resolution=(320, 240),framerate=60).start()
    vs = VideoStream(usePiCamera=args["picamera"] > 0, resolution=(640, 480),framerate=60).start()
    #vs = VideoStream(usePiCamera=args["picamera"] > 0, resolution=(640, 480),framerate=90).start()
    #vs = VideoStream(usePiCamera=args["picamera"] > 0, resolution=(1280, 720),framerate=60).start()
    #vs = VideoStream(usePiCamera=args["picamera"] > 0, resolution=(1640, 922),framerate=40).start()
    #vs = VideoStream(usePiCamera=args["picamera"] > 0, resolution=(1920, 1080),framerate=30).start()
    #vs = VideoStream(usePiCamera=args["picamera"] > 0, resolution=(1640, 1232),framerate=40).start()
    #vs = VideoStream(usePiCamera=args["picamera"] > 0, resolution=(3280, 2464),framerate=15).start()

def daMastaLoop():
