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
import cscore
#from pynput.keyboard import Key, Listener


from cscore import CameraServer
import imutils

# Import OpenCV and NumPy
import cv2
import numpy as np
from imutils.video import VideoStream

"""
<BEGIN> visionMAP  Sets global constants for codebase
"""
k_BALL_CAM_REZ_WIDTH = 640
k_BALL_CAM_REZ_HEIGHT = 480
k_BALL_CAM_FPS = 60 
k_CONVEYOR_CAM_REZ_WIDTH = 640
k_CONVEYOR_CAM_REZ_HEIGHT = 480
k_CONVEYOR_CAM_FPS = 30 
k_SHOOTER_CAM_REZ_WIDTH = 640
k_SHOOTER_CAM_REZ_HEIGHT = 480
k_SHOOTER_CAM_FPS = 60

k_NETWORKTABLES_SERVER_IP = "10.12.34.2"
"""
<END> visionMAP
"""


#vs = VideoStream(usePiCamera=args["picamera"] > 0, resolution=(3280, 2464),framerate=15).start()
#vs = VideoStream(usePiCamera=args["picamera"] > 0, resolution=(320, 240),framerate=60).start()
#vs = VideoStream(usePiCamera=True, resolution=(320, 240),framerate=60).start()
vs = VideoStream(usePiCamera=True, resolution=(k_BALL_CAM_REZ_WIDTH, k_BALL_CAM_REZ_HEIGHT),framerate=k_BALL_CAM_FPS).start()
#vs = VideoStream(usePiCamera=args["picamera"] > 0, resolution=(640, 480),framerate=60).start()
#vs = VideoStream(usePiCamera=True, resolution=(640, 480),framerate=90).start()
#vs = VideoStream(usePiCamera=args["picamera"] > 0, resolution=(1280, 720),framerate=60).start()
#vs = VideoStream(usePiCamera=args["picamera"] > 0, resolution=(1640, 922),framerate=40).start()
#vs = VideoStream(usePiCamera=args["picamera"] > 0, resolution=(1920, 1080),framerate=30).start()
#vs = VideoStream(usePiCamera=args["picamera"] > 0, resolution=(1640, 1232),framerate=40).start()

time.sleep(2.0)

def main():
    NetworkTables.initialize(server=k_NETWORKTABLES_SERVER_IP)

    vs.camera.brightness = 50
    vs.camera.contrast = 0
    vs.camera.saturation = 0

    cs = CameraServer.getInstance()
    ps = CameraServer.getInstance()
    cs.enableLogging()

    # Capture from the first USB Camera on the system
    #camera0 = cs.startAutomaticCapture()
    #camera1 = cs.startAutomaticCapture()
    #camera = cs.startAutomaticCapture(name="picam",path="/dev/v4l/by-path/platform-bcm2835-codec-video-index0")
    #camera = cs.startAutomaticCapture(name="usbcam",path="/dev/v4l/by-path/platform-fd500000.pcie-pci-0000:01:00.0-usb-0:1.2:1.0-video-index0")
    #camera0.setResolution(k_CONVEYOR_CAM_REZ_WIDTH, k_CONVEYOR_CAM_REZ_HEIGHT)
    camerausb = cscore.UsbCamera(name="usbcam",path="/dev/v4l/by-path/platform-fd500000.pcie-pci-0000:01:00.0-usb-0:1.2:1.0-video-index0")
    camerapi = cscore.CvSource("cvsource", cscore.VideoMode.PixelFormat.kMJPEG, k_BALL_CAM_REZ_WIDTH, k_BALL_CAM_REZ_HEIGHT, k_BALL_CAM_FPS)

    # setup MjpegServers
    usbMjpegServer = cscore.MjpegServer("ConveyorCam", 8081)
    piMjpegServer = cscore.MjpegServer("BallCam", 8082)

    # connect MjpegServers to their cameras
    usbMjpegServer.setSource(camerausb)
    piMjpegServer.setSource(camerapi)

    # Get a CvSink. This will capture images from the camera
    #cvSink = cs.getVideo()

    # (optional) Setup a CvSource. This will send images back to the Dashboard
    #outputStream = cs.putVideo("Name", k_BALL_CAM_REZ_WIDTH, k_BALL_CAM_REZ_HEIGHT)

    # Allocating new images is very expensive, always try to preallocate
    img = np.zeros(shape=(k_BALL_CAM_REZ_WIDTH, k_BALL_CAM_REZ_HEIGHT, 3), dtype=np.uint8)

    while True:
        frame = vs.read()
        camerapi.putFrame(frame)
        # Tell the CvSink to grab a frame from the camera and put it
        # in the source image.  If there is an error notify the output.
        #time, img = cvSink.grabFrame(img)
        #if time == 0:
        #    # Send the output the error.
        #    outputStream.notifyError(cvSink.getError());
        #    # skip the rest of the current iteration
        #    continue

        #
        # Insert image processing logic here
        #

        # (optional) send some image back to the dashboard
        #outputStream.putFrame(frame)
        #outputStream.putFrame(frame)
        print("putting Frame")


#vs.stop()

if __name__ == "__main__":
  main()

