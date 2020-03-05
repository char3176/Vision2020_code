# import the necessary packages
from __future__ import print_function
from imutils.video import VideoStream
import numpy as np
import argparse
import imutils
import time
import cv2
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
#ap.add_argument("-o", "--output", required=True, help="path to output video file")
ap.add_argument("-p", "--picamera", type=int, default=-1, help="whether or not the Raspberry Pi camera should be used")
#ap.add_argument("-f", "--fps", type=int, default=20, help="FPS of output video")
#ap.add_argument("-c", "--codec", type=str, default="MJPG", help="codec of output video")
args = vars(ap.parse_args())

# initialize the video stream and allow the camera
# sensor to warmup
print("[INFO] warming up camera...")
#vs = VideoStream(usePiCamera=args["picamera"] > 0, resolution=(320, 240),framerate=60).start()
#fps = 60
#vs = VideoStream(usePiCamera=args["picamera"] > 0, resolution=(640, 480),framerate=60).start()
#fps = 60
vs = VideoStream(usePiCamera=args["picamera"] > 0, resolution=(640, 480),framerate=90).start()
fps = 90
#vs = VideoStream(usePiCamera=args["picamera"] > 0, resolution=(1280, 720),framerate=60).start()
#fps = 60
#vs = VideoStream(usePiCamera=args["picamera"] > 0, resolution=(1640, 922),framerate=40).start()
#fps = 40
#vs = VideoStream(usePiCamera=args["picamera"] > 0, resolution=(1920, 1080),framerate=30).start()
#fps = 30
#vs = VideoStream(usePiCamera=args["picamera"] > 0, resolution=(1640, 1232),framerate=40).start()
#fps = 40
#vs = VideoStream(usePiCamera=args["picamera"] > 0, resolution=(3280, 2464),framerate=15).start()
#fps = 15

time.sleep(2.0)
vs.camera.brightness = 50
vs.camera.contrast = 0
vs.camera.saturation = 0

# initialize the FourCC, video writer, dimensions of the frame, and
# zeros array
fourcc = cv2.VideoWriter_fourcc(*args["codec"])
writer = None
(h, w) = (None, None)
zeros = None

# loop over frames from the video stream
while True:
  # grab the frame from the video stream and resize it to have a
  # maximum width of 300 pixels
  frame = vs.read()
  #frame = imutils.resize(frame, width=300)
  # check if the writer is None
  if writer is None:
    timestamp = float(time.time())
    outputfilename = str("video_"+timestamp+".avi")
    # store the image dimensions, initialize the video writer,
    # and construct the zeros array
    (h, w) = frame.shape[:2]
    #writer = cv2.VideoWriter(args["output"], fourcc, args["fps"], (w * 2, h * 2), True)
    writer = cv2.VideoWriter(outputfilename, fourcc, fps, (w * 2, h * 2), True)
    zeros = np.zeros((h, w), dtype="uint8")

  # break the image into its RGB components, then construct the
  # RGB representation of each frame individually
  (B, G, R) = cv2.split(frame)
  R = cv2.merge([zeros, zeros, R])
  G = cv2.merge([zeros, G, zeros])
  B = cv2.merge([B, zeros, zeros])
  # construct the final output frame, storing the original frame
  # at the top-left, the red channel in the top-right, the green
  # channel in the bottom-right, and the blue channel in the
  # bottom-left
  output = np.zeros((h * 2, w * 2, 3), dtype="uint8")
  output[0:h, 0:w] = frame
  output[0:h, w:w * 2] = R
  output[h:h * 2, w:w * 2] = G
  output[h:h * 2, 0:w] = B
  # write the output frame to file
  writer.write(output)
  # show the frames
  cv2.imshow("Frame", frame)
  cv2.imshow("Output", output)
  key = cv2.waitKey(1) & 0xFF
  # if the `q` key was pressed, break from the loop
  if key == ord("q"):
    break
# do a bit of cleanup
print("[INFO] cleaning up...")
cv2.destroyAllWindows()
vs.stop()
writer.release()
