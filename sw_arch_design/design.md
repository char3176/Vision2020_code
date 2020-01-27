
# main.py
  - import global modules

  - define CameraConfigClass
    -> see CameraConfigClass.md
  - define VizConfigClass
    - class vars
      - team #
      - server <- Bool: will this run as networktable server or client?
      - cameraConfigs = object of CameraConfigClass
    - class methods
      - init class
        run load config_file fxn
      - load config_file into data into class vars
        - read config_file.json into linear array
        - populate class vars from linear array
        - instantiate 1 object of cameraConfigClass for each set
          of cameraConfig data
     
  
  - main fxn
    - instantiate VizConfigClass as vizConfig object
    - instantiate NetworkTablesInstance as ntabl object
    - if vizConfig.server=True:
        ntabl.startServer()
      else:
        nttabl.startClientTeam(vizConfig.team)
    - pull data via networktables from SmartDashboard
        sd = ntabl.getTable('SmartDashboard')
    - create webcam camServer / streamViewer objects for publishing cam
      video to SmartDashboard
    - begin master_control_loop
        - pull NetworkTables data
        - update driverCommands state
            - If bullseyeOn then drawBullseyeOnG2Cam
            - If showDist2G2 then drawDistTextOnG2Cam
            - If showDist2LB then drawDistTextOnLBCam
            - If autoFireG2Engage then 
            - If autoChaseBall 
            - If showDriverG2Cam then set videostream to G2Stream
            - If showDriverLBCam then set videostream to LBStream
        - for i in listOfCams
          - processFrame

          



  - autoChaseBall
    - process frame/image using IdBallsInImage; return array of Ball objects
    - chk IsBallThere True (ie is len(array of Ball Objects) > 0)
    - Order array of Ball objects from one with largest apparent radius to 
      lowest apparent radius
    - set Ball2Chase = 1st in array of Ball objects
    - calc dist to Ball2Chase
    - calc yaw to Ball2Chase
    - 

  - recogG2
    - process frame/image using IdG2InImage; return array of contours
    - for c in contour 
       - perform approxPolyDP
       - perform boundingRect (optional maybe)
       - if len(approxPolyDP output) = 8:
           - calc centroid of G2
           - create 4 arrays to store points: RT, RB, LB, LT
	   - Put points of approx in RT, RB, LB, or LT
           	- if a points x coord < x coord of centroid AND its 
           	  y coord < y coord of centroid it goes in LB 
	        - if a points x coord < than x coord of centroid AND its 
       		  y coord is less > y coord of centroid it goes in LT 
       		- if a points x coord > than x coord of centroid AND its 
       		  y coord is less > y coord of centroid it goes in RT 
       		- if a points x coord > than x coord of centroid AND its 
       		  y coord is less < y coord of centroid it goes in RB 
	   - Check that each RT, RB, LB, & LT have correct number of points
 		(ie, if total # pts = 8, each should have 2 sets of points
		     if total # = 4, each should have 1 set of points)
	   - For each RT, RB, LB, & LT, seperate into Inner & Outer
		- For sets in RT if RT[0[0]] < RT[1[0]] then
		  iRT=RT[0] & oRT=RT[1], else iRT=RT[1] & oRT=RT[0]
		- rinse & repeat for RB, LB, & LT
	   - Using inner points [iRT, iRB, iLB, iLT] calc:
		- ang_iRTRBLB
		- ang_iLTLBRB
		- ang_iLBLTRT
		- ang_iRBRTLT
		- distance_iLTRT
		- distance_iLBRB
		- distance_iLTLB
		- distance_iRTRB
		- distance_iLTRB
		- distance_iLBRT
	   - check if values of calculated angles and ratios of distances
  	     match a trapazoid
  	   - 
           
	  



###-###-###-
# Class G2
  - class variables
	- number of points (basically am I a 4pt or 8pt model of G2)
	- centroid
	- iRB, iRT, iLT, iLB, oRT, oRB, oLT, oLB  <- coords of points after
	  being classified 
	- ang_iRTRBLB
	- ang_iLTLBRB
	- ang_iLBLTRT
	- ang_iRBRTLT
	- distance_iLTRT
	- distance_iLTLB
	- distance_iRTRB
	- distance_iLTRB
	- distance_iLBRT
	

  - class methods
     	- calc angle 
	- calc pixel distance
	- 
	
           

# 



###-###-###-###-###-###-###-###-###-###-###-###-###-###-###-###-###-###-
# import the necessary packages
import argparse
import imutils
import cv2
 
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
args = vars(ap.parse_args())
 
# load the video
camera = cv2.VideoCapture(args["video"])
 
# keep looping
while True:
	# grab the current frame and initialize the status text
	(grabbed, frame) = camera.read()
	status = "No Targets"
 
	# check to see if we have reached the end of the
	# video
	if not grabbed:
		break
 
	# convert the frame to grayscale, blur it, and detect edges
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	blurred = cv2.GaussianBlur(gray, (7, 7), 0)
	edged = cv2.Canny(blurred, 50, 150)
 
	# find contours in the edge map
	cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)

	# loop over the contours
	for c in cnts:
		# approximate the contour
		peri = cv2.arcLength(c, True)
		approx = cv2.approxPolyDP(c, 0.01 * peri, True)
 
		# ensure that the approximated contour is "roughly" rectangular
		if len(approx) >= 4 and len(approx) <= 6:
			# compute the bounding box of the approximated contour and
			# use the bounding box to compute the aspect ratio
			(x, y, w, h) = cv2.boundingRect(approx)
			aspectRatio = w / float(h)
 
			# compute the solidity of the original contour
			area = cv2.contourArea(c)
			hullArea = cv2.contourArea(cv2.convexHull(c))
			solidity = area / float(hullArea)
 
			# compute whether or not the width and height, solidity, and
			# aspect ratio of the contour falls within appropriate bounds
			keepDims = w > 25 and h > 25
			keepSolidity = solidity > 0.9
			keepAspectRatio = aspectRatio >= 0.8 and aspectRatio <= 1.2
 
			# ensure that the contour passes all our tests
			if keepDims and keepSolidity and keepAspectRatio:
				# draw an outline around the target and update the status
				# text
				cv2.drawContours(frame, [approx], -1, (0, 0, 255), 4)
				status = "Target(s) Acquired"
 
				# compute the center of the contour region and draw the
				# crosshairs
				M = cv2.moments(approx)
				(cX, cY) = (int(M["m10"] // M["m00"]), int(M["m01"] // M["m00"]))
				(startX, endX) = (int(cX - (w * 0.15)), int(cX + (w * 0.15)))
				(startY, endY) = (int(cY - (h * 0.15)), int(cY + (h * 0.15)))
				cv2.line(frame, (startX, cY), (endX, cY), (0, 0, 255), 3)
				cv2.line(frame, (cX, startY), (cX, endY), (0, 0, 255), 3)

	# draw the status text on the frame
	cv2.putText(frame, status, (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
		(0, 0, 255), 2)
 
	# show the frame and record if a key is pressed
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF
 
	# if the 'q' key is pressed, stop the loop
	if key == ord("q"):
		break
 
# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
###-###-###-###-###-###-###-###-###-###-###-###-###-###-###-###-###-###-
