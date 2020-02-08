from imutils.video import VideoStream
import time
import cv2
import picamera
import imutils
import argparse
import numpy as np
import numpy as np
import cv2
#import sys


#dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
#board = cv2.aruco.CharucoBoard_create(5,7,.025,.0125,dictionary)
board = cv2.aruco.CharucoBoard_create(5,7, 0.0356, 0.02134,dictionary)
img = board.draw((200*5,200*7))

#Dump the calibration board to a file
cv2.imwrite('charuco.png',img)


#Start capturing images for calibration
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
#vs = VideoStream(usePiCamera=args["picamera"] > 0, resolution=(320, 240),framerate=60).start()
#vs = VideoStream(usePiCamera=args["picamera"] > 0).start()
time.sleep(2.0)
vs.camera.brightness = 50
vs.camera.contrast = 0
vs.camera.saturation = 0

#cap = cv2.VideoCapture(0)

allCorners = []
allIds = []
decimator = 0
#for i in range(300):

numImagesTaken = 0
print("Total of ",numImagesTaken," images taken.")
while True:
    #ret,frame = cap.read()
    frame = vs.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    [markerCorners,markerIds,rejectedImgPoints] = cv2.aruco.detectMarkers(gray,dictionary)
    #print("RES OUTPUT BEGIN")
    #print(res)
    #print("RES OUTPUT END")

        #print("RES2 OUTPUT BEGIN")
        #print(res2)
        #print("RES2 OUTPUT END")

        #if charucoCorners is not None and charucoIds is not None and len(charucoCorners)>3 and decimator%3==0:
        #    allCorners.append(charucoCorners)
        #    allIds.append(charucoIds)
        #    numImagesTaken+=1

    if len(markerCorners)>0:
      [ret,charucoCorners, charucoIds] = cv2.aruco.interpolateCornersCharuco(markerCorners,markerIds,gray,board)
      cv2.aruco.drawDetectedMarkers(gray, markerCorners, markerIds)
      cv2.aruco.drawDetectedCornersCharuco(gray,charucoCorners,charucoIds)

    cv2.imshow('frame',gray)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('c'):
      if len(markerCorners)>0:
        [ret,charucoCorners, charucoIds] = cv2.aruco.interpolateCornersCharuco(markerCorners,markerIds,gray,board)
        #if charucoCorners is not None and charucoIds is not None and len(charucoCorners)>3 and decimator%3==0:
        if charucoCorners is not None and charucoIds is not None and len(charucoCorners)>3:
            allCorners.append(charucoCorners)
            allIds.append(charucoIds)
            numImagesTaken+=1
            print("Total of ",numImagesTaken," images taken.")
    decimator+=1

imsize = gray.shape

#Calibration fails for lots of reasons. Release the video if we do
try:
    [ret,cameraMatrix,distortionCoeffs,rvecs,tvecs, stdDeviationsIntrinsics, stdDeviationsExtrinsics, perViewErrors] = cv2.aruco.calibrateCameraCharucoExtended(allCorners,allIds,board,imsize,None,None)
    #[ret,cameraMatrix,distortionCoeffs,rvecs,tvecs] = cv2.aruco.calibrateCameraCharuco(allCorners,allIds,board,imsize,None,None)
    print("Using ",numImagesTaken," images/frames")
    print("Rep Error:", ret)
    print("Camera Matrix:", cameraMatrix)
    print("Distortion Coefficients:", distortionCoeffs)
    #print("stdDeviationsExtrinsics:",stdDeviationsExtrinsics)
    #print("perViewErrors:",perViewErrors)
except ValueError as e:
    print(e)
except NameError as e:
    print(e)
except AttributeError as e:
    print(e)
except:
    print("calibrateCameraCharuco failed: ", sys.exc_info()[0])



cv2.destroyAllWindows()
vs.stop()
