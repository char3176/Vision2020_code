import cv2
import math

class G2Class:


    def __init__(self, cnt, approx, G2ID, frame):

        #Booleans
        self.isAG2 = False
        self.isInRingOfFire = False

        #Crap
        self.originalFrame = frame.copy()
        self.newframe = frame
        self.cnt = cnt
        self.approx = approx[G2ID]
        self.G2ID = G2ID
        self.approxPts = []
        self.centroid = []
        self.cX = 0
        self.cY = 0

        # Quadrant Points
        self.RTpts = []
        self.LTpts = []
        self.LBpts = []
        self.RBpts = []

        #Averages of quadrants
        self.avgPts = []
        #Vision Tape Ratio Constant
        self.upperOverLowerRatio = 1.69

        #print("__init__: approx: ",approx)
        #Checking if pointset has 4 or 8 elements
        #print("len(self.approx) == 4 or len(self.approx[) >= 8")
        #print(len(self.approx) == 4, "or", len(self.approx) >= 8)
        if len(self.approx) == 4 or len(self.approx) >= 8:
            #Loops over points
            numOfPoints = len(self.approx)
            #print("__init__: numOfPoints = ", numOfPoints)
            for pointsIndex in range(0, numOfPoints):
                coordArray = self.approx[pointsIndex][0]
                coordArray2 = coordArray.tolist()
                self.approxPts.append(coordArray2)
        #print("__init__: approxPts: ", self.approxPts)

      ##### NEED TO FIX APPROXPTS ARRAY ABOVE TO INCLUDE/ACCOUNT FOR MULTIPE ---should be accounted for with
      ##### "PtsSets" incase of more than 1 contour
      ##### ANNNDDDD decide what to do if we are fu-bar'd with more than one match later
      ##### lower down in Jake's logic

    def calcCentroid(self):
        #Compute the centroid of the array of approxPts
        #print(self.approxPts)
        M = cv2.moments(self.cnt)
        #print(M)
        self.cX = int(M["m10"] / M["m00"])
        self.cY = int(M["m01"] / M["m00"])
        #print("calcCentroid: ",self.cX,self.cY)
        self.centroid = [self.cX, self.cY]


    def hasEqualQuadrants(self, numOfPoints):
        if len(self.RTpts) == numOfPoints and len(self.LTpts) == numOfPoints and len(self.LBpts) == numOfPoints and len(self.RBpts) == numOfPoints:
            #print("NumPoints in RT, LT, LB, RB : ",len(self.RTpts), len(self.LTpts), len(self.LBpts), len(self.RBpts))
            #print("hasEqualQuadrants = True")
            return True
        else:
            #print("RT: ", self.RTpts)
            #print("LT: ", self.LTpts)
            #print("LB: ", self.LBpts)
            #print("RB: ", self.RBpts)
            #print("NumPoints in RT, LT, LB, RB : ",len(self.RTpts), len(self.LTpts), len(self.LBpts), len(self.RBpts))
            #print("hasEqualQuadrants =  False")
            return False


    def getAveragePoint(self, pointList):
        pointTotal = 0
        totalX = 0
        totalY = 0
        for point in pointList:
            pointTotal += 1
            totalX += point[0]
            totalY += point[1]
        return [(int)(totalX / pointTotal), (int)(totalY / pointTotal)]



    def seperateIntoQuads(self):
        if (len(self.approxPts) == 4 and self.hasEqualQuadrants(1)) or len(self.approxPts) >= 8:
            #print("seperateIntoQuads: self.approxPts: ", self.approxPts)
            for pnt in self.approxPts:
                if pnt[0] > self.cX:
                    if pnt[1] < self.cY:
                        self.RTpts.append(pnt)
                    else:
                        self.RBpts.append(pnt)
                else:
                    if pnt[1] < self.cY:
                        self.LTpts.append(pnt)
                    else:
                        self.LBpts.append(pnt)
        #print("seperateIntoQuads: self.RTpts: ",self.RTpts)
        #print("seperateIntoQuads: self.LTpts: ",self.LTpts)
        #print("seperateIntoQuads: self.LBpts: ",self.LBpts)
        #print("seperateIntoQuads: self.RBpts: ",self.RBpts)


    def findAvgs(self):
        if len(self.approxPts) >= 8:
            if len(self.RTpts) > 0:
                self.avgPts.append(self.getAveragePoint(self.RTpts))
            if len(self.LTpts) > 0:
                self.avgPts.append(self.getAveragePoint(self.LTpts))
            if len(self.LBpts) > 0:
                self.avgPts.append(self.getAveragePoint(self.LBpts))
            if len(self.RBpts) > 0:
                self.avgPts.append(self.getAveragePoint(self.RBpts))
        elif self.hasEqualQuadrants(1):
            #If 1 point per quadrant, make the average our only point
            self.avgPts.append(self.RTpts)
            self.avgPts.append(self.LTpts)
            self.avgPts.append(self.LBpts)
            self.avgPts.append(self.RBpts)
            #print("avgRTpts: ", self.avgPts[0])
            #print("avgLTpts: ", self.avgPts[1])
            #print("avgLBpts: ", self.avgPts[2])
            #print("avgRBpts: ", self.avgPts[3])
            #print("Centroid: ", self.centroid)\
        else:
            self.isAG2 = False


    def calcDistance(self,point1, point2):
        xDiff = point1[0] - point2[0]
        yDiff = point1[1] - point2[1]
        dist = math.sqrt((xDiff * xDiff) + (yDiff * yDiff))
        return dist

    def amIG2(self):
        #Run tests if the quadrant test passed
            #print("isAG2 initial: ", self.isAG2)
        #if self.isAG2:
            #FIND THE FIRST TWO ANGLES
            #Find longest side using the di
            if len(self.avgPts) == 4:
              LTtoRTImgDist = self.calcDistance(self.avgPts[1], self.avgPts[3])
              #Find shortest side using the distance formula
              xDiff = self.avgPts[2][0] - self.avgPts[3][0]
              yDiff = self.avgPts[2][1] - self.avgPts[3][1]
              LBtoRBImgDist = math.sqrt((xDiff * xDiff) + (yDiff * yDiff))
              #Find the ratio
              distRatioImg = LTtoRTImgDist / LBtoRBImgDist
            #If ratios aren't similar, we're not looking at a G2
              if abs(distRatioImg - self.upperOverLowerRatio) < 0.15:
                self.isAG2 = True

            #Go to next text if it passed the first
              if self.isAG2:
                #Eq1 refers to line equation of the line between Quads 2 and 4
                #Eq2 refers to the equation of the perp line between Quad 3
                    #and the point of intersection of eq1
                #Calculate the y=mx+b equation of eq1
                deltaY = self.avgPts[3][1] - self.avgPts[1][1]
                deltaX = self.avgPts[3][0] - self.avgPts[1][0]
                slopeEq1 = deltaY/deltaX
                yIntEq1 = self.avgPts[1][1] - (slopeEq1 * self.avgPts[1][0])
                #Calculate the y=mx+b equation of eq2 using point slope
                slopeEq2 = -deltaX/deltaY
                yIntEq2 =  self.avgPts[2][1] + (-slopeEq2 * self.avgPts[2][0])
                #Calculate the intersection point of Eq1 and Eq2
                xInt = (int)((yIntEq2 - yIntEq1) / (slopeEq1 - slopeEq2))
                yInt = (int)(slopeEq1 * xInt) + yIntEq1
                #Find the three side lengths
                Q2toQ3 = self.calcDistance(self.avgPts[1], self.avgPts[2])
                Q3toQ4 = self.calcDistance(self.avgPts[2], self.avgPts[3])
                sharedSide = self.calcDistance(self.avgPts[2], [xInt, yInt])
                #Use trig to calculate angles
                ang1 = 90 - math.degrees(math.sin(sharedSide / Q2toQ3))
                ang2 = 90 - math.degrees(math.sin(sharedSide / Q3toQ4))

                #FIND THE SECOND TWO ANGLES
                #Eq1 refers to line equation of the line between Quads 2 and 4
                #Eq2 refers to the equation of the perp line between Quad 3
                    #and the point of intersection of eq1
                #Calculate the y=mx+b equation of eq1
                deltaY = self.avgPts[2][1] - self.avgPts[0][1]
                deltaX = self.avgPts[2][0] - self.avgPts[0][0]
                slopeEq1 = deltaY/deltaX
                yIntEq1 = self.avgPts[2][1] - (slopeEq1 * self.avgPts[2][0])
                #Calculate the y=mx+b equation of eq2 using point slope
                slopeEq2 = -deltaX/deltaY
                yIntEq2 =  self.avgPts[3][1] + (-slopeEq2 * self.avgPts[3][0])
                #Calculate the intersection point of Eq1 and Eq2
                xInt = (int)((yIntEq2 - yIntEq1) / (slopeEq1 - slopeEq2))
                yInt = (int)(slopeEq1 * xInt) + yIntEq1
                #Find the three side lengths
                Q3toQ4 = self.calcDistance(self.avgPts[2], self.avgPts[3])
                Q4toQ1 = self.calcDistance(self.avgPts[3], self.avgPts[0])
                sharedSide = self.calcDistance(self.avgPts[3], [xInt, yInt])
                #Use trig to calculate angles
                ang3 = 90 - math.degrees(math.sin(sharedSide / Q3toQ4))
                ang4 = 90 - math.degrees(math.sin(sharedSide / Q4toQ1))

                #Check if the angles' sum are around 250 degrees because its usually 250 for some reason
                if abs((ang1 + ang2 + ang3 + ang4) - 250) >= 15:
                    self.isAG2 = False
                #print("Sum of angles: ", ang1 + ang2 + ang3 + ang4)
                #print("distRatioImg: ", distRatioImg, "upperOverLowerRatio ", self.upperOverLowerRatio)

    def calcIfInRingOfFire(self, frame, ringOfFireRadiusScale = 0.05):
        width = frame.shape[1]
        height = frame.shape[0]
        centerOfFrame = [int(width/2),int(height/2)]
        distance = self.calcDistance(self.centroid, centerOfFrame)
        #print("width = ", width, "height = ", height)
        #print("Distance to ROF: ", distance, "ROF Threshold: ", (ringOfFireRadiusScale * (0.5 * height)))
        if distance < (ringOfFireRadiusScale * (0.5 * height)):
            self.isInRingOfFire = True

    def drawFittingOnFrame(self, frame):
        #*#*#*  Need to loop over approx "len(approx)" times doing below conditional
        tempimage = frame.copy()
        red = [0,0,255]
        #cv2.circle(tempimage, (int(100), int(100)), int(30), (0,255,0), 2)
        #print("tempimage: ",tempimage)
        #print("tempimage len: ",len(tempimage))
        #print("tempimage[0] len: ",len(tempimage[0]))
        approxPtsLength = len(self.approxPts)
        #print(approxPtsLength)
        for i in range(0,approxPtsLength):
          #print("i: ", i)
          #print(self.approxPts[i][0],self.approxPts[i][1])
          #print(tempimage[self.approxPts[i][1],self.approxPts[i][0]])
          tempimage[self.approxPts[i][1],self.approxPts[i][0]]=red
        cv2.drawContours(tempimage, [self.approx], -1, (0, 0, 255), 2)
        cv2.drawContours(tempimage, self.approx, -1, (0, 255, 0), 4)
        M = cv2.moments(self.cnt)
#        #print(M)
        self.cX = int(M["m10"] / M["m00"])
        cX = int(M["m10"] / M["m00"])
        self.cY = int(M["m01"] / M["m00"])
        cY = int(M["m01"] / M["m00"]) - 20
#        #print(self.cX,self.cY)
        self.centroid = [self.cX, self.cY]
        (x, y, w, h) = cv2.boundingRect(self.approx)
        (startX, endX) = (int(cX - (h * 0.25)), int(cX + (h * 0.25)))
        (startY, endY) = (int(cY - (h * 0.25)), int(cY + (h * 0.25)))
        cv2.line(tempimage, (startX, cY), (endX, cY), (0, 255, 0), 2)
        cv2.line(tempimage, (cX, startY), (cX, endY), (0, 255, 0), 2)
        myradius = ((endY - startY) / 2 ) * 0.8
        cv2.circle(tempimage, (int(cX), int(cY)), int(myradius), (0,255,0), 1)
        cv2.circle(tempimage, (int(cX), int(cY)), int(myradius * 0.3), (0,0,255), 1)
        return tempimage

    def drawCircleOnFrame(self):
        #*#*#*  Need to loop over approx "len(approx)" times doing below conditional
        #print("approx:",approx)
        cv2.circle(self.newframe, (int(100), int(100)), int(30), (0,255,0), 2)

    def doEverything(self):
        print()
        #print("COUNTOUR ", self.G2ID, "BEGINS!!")
        #cv2.drawContours(self.newframe, self.cnt, -1, (0,255,0), 3)
        #cv2.drawContours(self.newframe, [self.cnt], -1, (0,0,255), 3)
        self.calcCentroid()
        self.seperateIntoQuads()
        self.findAvgs()
        self.amIG2()
        self.calcIfInRingOfFire(self.originalFrame, 0.25)
        #if self.isAG2:
        #  frame = self.drawFittingOnFrame(frame)
        print("Is a G2: ", self.isAG2)
        #print("IsInROF: ", self.isInRingOfFire)
        print("Total points: ", len(self.approxPts))
        #print("END OF CONTOUR ", self.G2ID, "!!")

