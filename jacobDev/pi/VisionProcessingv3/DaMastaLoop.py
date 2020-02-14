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
import time
import logging
from networktables import NetworkTables
from networktables import NetworkTablesInstance
import RPi.GPIO as GPIO

#CAMERA IMPORTS
import picamera
from imutils.video import VideoStream

#CLASS IMPORTS
import VisionProcessing as vp

#Set up controllable LED
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO_PIN = 23
GPIO.setup(GPIO_PIN, GPIO.OUT)

#Set up the network table
ntinst = NetworkTablesInstance.getDefault()
#ntinst.startClientTeam(3176)
netTable = NetworkTables.getTable("SmartDashBoard")
#netTable.initialize(server='10.12.34.2') not sure we need this

logging.basicConfig(
    filename="vision.log",
    level=logging.DEBUG,
    format="%(asctime)s:%(levelname)s:%(messages)s"
    )

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

def daMastaLoop():
    isLightOn = False
    while True:
    #Grab the frame
        frame = vs.read()

        #frame = VisionProcessing(frame)
        cv2.imshow("VP", frame)
        #---------------------#
        #STEP 1: GET TABLE DATA
        #---------------------#
        #netTable = 

        #-----------------------------------#
        #STEP 2: MAKE DECISIONS BASED ON DATA
        #-----------------------------------#
        g2 = vp.findG2InFrame(frame)
        if g2 is not None:
            frame = g2.drawFittingOnFrame(frame)
            angle = g2.calcAngle()
            dist = g2.calcRange()
            #print("Ang: ", angle, " Range(in): ", dist[0] / 0.0254)
            print("R1: ", dist[0] / 0.0254, " R2: ", dist[1] / 0.0254)


        key = cv2.waitKey(1) & 0xFF

        if key == ord("l"): #LED
            isLightOn = not isLightOn
        elif key == ord("k"): #Kill
            break
    
        if isLightOn:
            GPIO.output(GPIO_PIN, GPIO.HIGH)
        else:
           GPIO.output(GPIO_PIN, GPIO.LOW)

        #------------------------#
        #STEP 3: UPDATE TABLE DATA
        #------------------------#
        ntinst.flush()

    GPIO.output(GPIO_PIN, GPIO.LOW)  

daMastaLoop()
cv2.destroyAllWindows()
vs.stop()

