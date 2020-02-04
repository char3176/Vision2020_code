
# import the necessary packages
from collections import deque
import numpy as np
import argparse
import imutils
import cv2

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
#ap.add_argument("-v", "--video", help="path to the (optional) video file")
ap.add_argument("-i", "--input", help="path to the input image file")
ap.add_argument("-b", "--buffer", type=int, default=64, help="max buffer size")
args = vars(ap.parse_args())

# define the lower and upper boundaries of the "yellow object"
# (or "ball") in the HSV color space, then initialize the
# list of tracked points
colorLower = (24, 100, 100)
colorUpper = (44, 255, 255)
pts = deque(maxlen=args["buffer"])

# if a video path was not supplied, grab the reference
# to the webcam
#if not args.get("video", False):
#  camera = cv2.VideoCapture(0)

# otherwise, grab a reference to the video file
#else:
#  camera = cv2.VideoCapture(args["video"])
frame = cv2.imread(args["input"])

# keep looping
#while True:
  # grab the current frame
#  (grabbed, frame) = camera.read()

  # if we are viewing a video and we did not grab a frame,
  # then we have reached the end of the video
#  if args.get("video") and not grabbed:
#    break

  # resize the frame, inverted ("vertical flip" w/ 180degrees),
  # blur it, and convert it to the HSV color space
frame = imutils.resize(frame, width=640)
  #frame = imutils.rotate(frame, angle=180)

  # blurred = cv2.GaussianBlur(frame, (11, 11), 0)
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
hsv = cv2.bilateralFilter(hsv, 5, 175, 175)

  # construct a mask for the color of the ball, then perform
  # a series of dilations and erosions to remove any small
  # blobs left in the mask
mask = cv2.inRange(hsv, colorLower, colorUpper)
mask = cv2.erode(mask, None, iterations=2)
mask = cv2.dilate(mask, None, iterations=2)

#frame_orig = frame.copy()
#gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#bilateral_filtered_frame = cv2.bilateralFilter(frame, 5, 175, 175)
#gray = bilateral_filtered_frame.copy()
#edges = cv2.Canny(gray, 300, 500)
#circles = cv2.HoughCircles(edges, cv2.HOUGH_GRADIENT, 1, gray.shape[0]/2, param1=200, param2=10, minRadius=5, maxRadius=80)
#if circles is not None:
#  circles = np.round(circles[0, :]).astype("int")
#  for (x, y, r) in circles:
#    cv2.circle(gray, (x, y), r, (0, 255, 0), 4)
#    cv2.rectangle(gray, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
#  #cv2.imshow("the circles", np.hstack([edges, gray]))
#  cv2.imshow("the circles", gray)
#  cv2.waitKey(0)
  # find contours in the mask and initialize the current
  # (x, y) center of the ball
cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
center = None
print ("Num contours on ", args["input"], " = ", len(cnts))


# draw all found contours
if len(cnts) > 0:
  for i in range(0, len(cnts)):
      ((x, y), radius) = cv2.minEnclosingCircle(cnts[i])
      M = cv2.moments(cnts[i])
      center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
      cv2.drawContours(frame, [cnts[i]], 0, (0, 255, 0), 3)

  # only proceed if at least one contour was found
if len(cnts) > 0:
    # find the largest contour in the mask, then use
    # it to compute the minimum enclosing circle and
    # centroid
  c = max(cnts, key=cv2.contourArea)
  ((x, y), radius) = cv2.minEnclosingCircle(c)
  M = cv2.moments(c)
  center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
  print (M)
  #eccentricity = (((((M["m20"]) - (M["m02"]))**2) - ((4 * ((M["m11"])**2)))) / (((M["m20"]) + ((M["m02"])))**2))
  #print("Eccentricity = ",eccentricity)

    # only proceed if the radius meets a minimum size
  if radius > 10:
    c = max(cnts, key=cv2.contourArea)
      # draw the circle and centroid on the frame,
      # then update the list of tracked points
    cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
    cv2.circle(frame, center, 5, (0, 0, 255), -1)
  # update the points queue
  pts.appendleft(center)

    # loop over the set of tracked points
  for i in range(1, len(pts)):
    # if either of the tracked points are None, ignore
    # them
    if pts[i - 1] is None or pts[i] is None:
      continue

    # otherwise, compute the thickness of the line and
    # draw the connecting lines
    thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
    cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)

    # put text (cntStr) at bottom left of image telling num of contours
  cntStr = str("Contours: " + str(len(cnts)))
  radiusStr = str("Radius: " + str(round(radius,3)))
  frameDimensions = frame.shape
  frameHeight = frame.shape[0]
  frameWidth = frame.shape[1]
  frameNumElementsPerPixel = frame.shape[2]
  frameYStartPtForText = (frameHeight - 10)
  frameXStartPtForText = 10
  frameFont = cv2.FONT_HERSHEY_COMPLEX_SMALL
  frameFontScale = 0.8
  frameFontColor = (0,255,0)
  frameLineType = 1
  cv2.putText(frame,cntStr,(frameXStartPtForText, frameYStartPtForText - 0),frameFont, frameFontScale, frameFontColor, frameLineType)
  cv2.putText(frame,radiusStr,(frameXStartPtForText, frameYStartPtForText - 15),frameFont, frameFontScale, frameFontColor, frameLineType)

  # show the frame to our screen
while True:
  cv2.imshow("Frame", frame)
  key = cv2.waitKey(1) & 0xFF
  # if the 'q' key is pressed, stop the loop
  if key == ord("q"):
     break
outputfilename = str("contours_marked/"+args["input"])+"_"+str(len(cnts))+"contours.jpg"
cv2.imwrite(outputfilename, frame)

# cleanup the camera and close any open windows
#camera.release()
#cv2.destroyAllWindows()

