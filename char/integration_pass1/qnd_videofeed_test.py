# Import the camera server
import cv2
import numpy as np
import argparse
from collections import deque
import sys
import picamera
from imutils.video import VideoStream
import time
import math
import cv2
import time
import math
import logging
from networktables import NetworkTables
from networktables import NetworkTablesInstance
from cscore import CameraServer, VideoSource
#from pynput.keyboard import Key, Listener


from cscore import CameraServer
import imutils

# Import OpenCV and NumPy
import cv2
import numpy as np
from imutils.video import VideoStream


#vs = VideoStream(usePiCamera=args["picamera"] > 0, resolution=(3280, 2464),framerate=15).start()
#vs = VideoStream(usePiCamera=args["picamera"] > 0, resolution=(320, 240),framerate=60).start()
#vs = VideoStream(usePiCamera=args["picamera"] > 0, resolution=(640, 480),framerate=60).start()
vs = VideoStream(usePiCamera=True, resolution=(640, 480),framerate=90).start()
#vs = VideoStream(usePiCamera=args["picamera"] > 0, resolution=(1280, 720),framerate=60).start()
#vs = VideoStream(usePiCamera=args["picamera"] > 0, resolution=(1640, 922),framerate=40).start()
#vs = VideoStream(usePiCamera=args["picamera"] > 0, resolution=(1920, 1080),framerate=30).start()
#vs = VideoStream(usePiCamera=args["picamera"] > 0, resolution=(1640, 1232),framerate=40).start()
time.sleep(2.0)

#def on_release(key):
#    if key == Key.esc:
#        # Stop Listener
#        return False

def main():
    NetworkTables.initialize(server='10.12.34.2')
    vs.camera.brightness = 50
    vs.camera.contrast = 0
    vs.camera.saturation = 0

    cs = CameraServer.getInstance()
    cs.enableLogging()

    # Capture from the first USB Camera on the system
    camera0 = cs.startAutomaticCapture()
    #camera1 = cs.startAutomaticCapture()
    #camera = cs.startAutomaticCapture(name="picam",path="/dev/v4l/by-path/platform-bcm2835-codec-video-index0")
    camera0.setResolution(640, 480)

    # Get a CvSink. This will capture images from the camera
    cvSink = cs.getVideo()

    # (optional) Setup a CvSource. This will send images back to the Dashboard
    outputStream = cs.putVideo("Name", 640, 480)

    # Allocating new images is very expensive, always try to preallocate
    imgb = np.zeros(shape=(640, 480, 3), dtype=np.uint8)
    img = np.zeros(shape=(640, 480, 3), dtype=np.uint8)

    while True:
        frame = vs.read()
        # Tell the CvSink to grab a frame from the camera and put it
        # in the source image.  If there is an error notify the output.
        time, img = cvSink.grabFrame(img)
        if time == 0:
            # Send the output the error.
            outputStream.notifyError(cvSink.getError());
            # skip the rest of the current iteration
            continue

        #
        # Insert image processing logic here
        #

        # (optional) send some image back to the dashboard
        #outputStream.putFrame(frame)
        outputStream.putFrame(img)
        print("putting Frame")


#vs.stop()

if __name__ == "__main__":
  main()

