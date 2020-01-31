import cv2
import math

class G2Class:


    def __init__(self, cnt, approx):
        self.isAG2 = False

        self.cnts = cnt
        self.approx = approx[0]
        self.approxPts = []
        self.centroid = []
        self.cX = 0
        self.cY = 0

        # Quadrant Points
        self.RTpts = []
        self.LTpts = []
        self.LBpts = []
        self.RBpts = []

        #Outer Points
        self.outerPts = []
        #Inner Points
        self.innerPts = []
        #Averages
        self.avgPts = []
        self.test1 = []
        #Vision Tape Constants
        self.LTtoRTLen = 39.25
        #Average between inner and outer lengths
        self.sideLen = (17.5 + 19.625) / 2
        #*#*#*  Need to loop over approx "len(approx)" times doing below conditional
        numOfPointSets = len(approx)
        #Loops over pointsets
        print("approx:",approx)
        for pointSetIndex in range(0,numOfPointSets):
   	    #Checking if pointset has 4 or 8 elements
           if len(approx[pointSetIndex]) == 4 or 8:
                #Loops over points
                numOfPoints = len(approx[pointSetIndex])
                for pointsIndex in range(0, numOfPoints):
                    coordArray = approx[pointSetIndex][pointsIndex][0]
                    coordArray2 = coordArray.tolist()
                    self.approxPts.append(coordArray2)
        print("approxPts", self.approxPts)
        red = [0,0,255]
        tempimage = cv2.imread("test.jpg")
        print("tempimage: ",tempimage)
        print("tempimage len: ",len(tempimage))
        print("tempimage[0] len: ",len(tempimage[0]))
        approxPtsLength = len(self.approxPts)
        print(approxPtsLength)
        for i in range(0,approxPtsLength):
          print("i: ", i)
          print(self.approxPts[i][0],self.approxPts[i][1])
          print(tempimage[self.approxPts[i][1],self.approxPts[i][0]])
          tempimage[self.approxPts[i][1],self.approxPts[i][0]]=red
        cv2.drawContours(tempimage, [self.approx], -1, (0, 0, 255), 2)
        cv2.drawContours(tempimage, self.approx, -1, (0, 255, 0), 4)
        cnt = self.cnts[0]
        M = cv2.moments(cnt)
        print(M)
        self.cX = int(M["m10"] / M["m00"])
        cX = int(M["m10"] / M["m00"])
        self.cY = int(M["m01"] / M["m00"])
        cY = int(M["m01"] / M["m00"]) - 20
        print(self.cX,self.cY)
        self.centroid = [self.cX, self.cY]
        (x, y, w, h) = cv2.boundingRect(self.approx)
        (startX, endX) = (int(cX - (h * 0.25)), int(cX + (h * 0.25)))
        (startY, endY) = (int(cY - (h * 0.25)), int(cY + (h * 0.25)))
        cv2.line(tempimage, (startX, cY), (endX, cY), (0, 255, 0), 2)
        cv2.line(tempimage, (cX, startY), (cX, endY), (0, 255, 0), 2)
        myradius = ((endY - startY) / 2 ) * 0.8
        cv2.circle(tempimage, (int(cX), int(cY)), int(myradius), (0,255,0), 1)
        cv2.circle(tempimage, (int(cX), int(cY)), int(myradius * 0.3), (0,0,255), 1)
        cv2.imwrite('t.jpg',tempimage)


      ##### NEED TO FIX APPROXPTS ARRAY ABOVE TO INCLUDE/ACCOUNT FOR MULTIPE
      ##### "PtsSets" incase of more than 1 contour
      ##### ANNNDDDD decide what to do if we are fu-bar'd with more than one match later
      ##### lower down in Jake's logic

    def calcCentroid(self):
        #Compute the centroid of the array of approxPts
        #print(self.approxPts)
        cnt = self.cnts[0]
        M = cv2.moments(cnt)
        print(M)
        self.cX = int(M["m10"] / M["m00"])
        self.cY = int(M["m01"] / M["m00"])
        print(self.cX,self.cY)
        self.centroid = [self.cX, self.cY]

    def seperateIntoQuads(self):
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

    def seperateQuadsIntoIvO(self):
        if len(self.approxPts) == 8:
            #Quadrant 1: RT
            if self.RTpts[0][0] > self.RTpts[1][0]:
                self.innerPts.append(self.RTpts[0])
                self.outerPts.append(self.RTpts[1])
            else:
                self.innerPts.append(self.RTpts[1])
                self.outerPts.append(self.RTpts[0])

            #Quadrant 2: LT
            if self.LTpts[0][0] > self.LTpts[1][0]:
                self.innerPts.append(self.LTpts[0])
                self.outerPts.append(self.LTpts[1])
            else:
                self.innerPts.append(self.LTpts[1])
                self.outerPts.append(self.LTpts[0])

            #Quadrant 3: LB
            if self.LBpts[0][0] > self.LBpts[1][0]:
                self.innerPts.append(self.LBpts[0])
                self.outerPts.append(self.LBpts[1])
            else:
                self.innerPts.append(self.LBpts[1])
                self.outerPts.append(self.LBpts[0])

            #Quadrant 4: RB
            if self.RBpts[0][0] > self.RBpts[1][0]:
                self.innerPts.append(self.RBpts[0])
                self.outerPts.append(self.RBpts[1])
            else:
                self.innerPts.append(self.RBpts[1])
                self.outerPts.append(self.RBpts[0])
            print("RTpts: ",self.RTpts)
            print("RBpts: ",self.RBpts)
            print("LBpts: ",self.LBpts)
            print("LTpts: ",self.LTpts)

    def findAvgs(self):
        if len(self.RTpts) == 2:
            #Average the two points in each quadrant
            XCoord = (int)(self.RTpts[0][0] + self.RTpts[1][0])/2
            YCoord = (int)(self.RTpts[0][1] + self.RTpts[1][1])/2
            self.avgPts.append([XCoord, YCoord])
            XCoord = (int)(self.LTpts[0][0] + self.LTpts[1][0])/2
            YCoord = (int)(self.LTpts[0][1] + self.LTpts[1][1])/2
            self.avgPts.append([XCoord, YCoord])
            XCoord = (int)(self.LBpts[0][0] + self.LBpts[1][0])/2
            YCoord = (int)(self.LBpts[0][1] + self.LBpts[1][1])/2
            self.avgPts.append([XCoord, YCoord])
            XCoord = (int)(self.RBpts[0][0] + self.RBpts[1][0])/2
            YCoord = (int)(self.RBpts[0][1] + self.RBpts[1][1])/2
            self.avgPts.append([XCoord, YCoord])
        else:
            #If 1 point per quadrant, make the average our only point
            self.avgPts.append(RTpts)
            self.avgPts.append(LTpts)
            self.avgPts.append(LBpts)
            self.avgPts.appemd(RBpts)
        print("avgRTpts: ",self.RTpts)
        print("RBpts: ",self.RBpts)
        print("LBpts: ",self.LBpts)
        print("LTpts: ",self.LTpts)

    def calcDistance(self,point1, point2):
        xDiff = point1[0] - point2[0]
        yDiff = point1[1] - point2[1]
        dist = math.sqrt((xDiff * xDiff) + (yDiff * yDiff))
        return dist

    def amIG2(self):
        #FIND THE FIRST TWO ANGLES
        #Find longest side using the distance formula
        self.LTtoRTImgDist = self.calcDistance(self.avgPts[1], self.avgPts[3])
        #Find shortest side using the distance formula
        xDiff = self.avgPts[2][0] - self.avgPts[3][0]
        yDiff = self.avgPts[2][1] - self.avgPts[3][1]
        self.LBtoRBImgDist = math.sqrt((xDiff * xDiff) + (yDiff * yDiff))
        #Find the ratio
        distRatioImg = self.LTtoRTImgDist/self.LBtoRBImgDist
        distRatioReal = self.LTtoRTLen / self.sideLen
        #If ratios aren't similar, we're not looking at a G2
        if abs(distRatioImg - distRatioReal) < 0.1:
           self.isAG2 = True
           print("self.isAG2: ")
        #Go to next text if it passed the first
        if self.isAG2:
            #Eq1 refers to line equation of the line between Quads 2 and 4
            #Eq2 refers to the equation of the perp line between Quad 3
                #and the point of intersection of eq1
            #Calculate the y=mx+b equation of eq1
            deltaY = self.avgPts[3][1] - self.avgPts[1][1]
            deltaX = self.avgPts[3][0] - self.avgPts[1][0]
            slopeEq1 = deltaY/deltaX
            yIntEq1 = slope * self.avgPts[1][0]
            #Calculate the y=mx+b equation of eq2 using point slope
            slopeEq2 = -deltaX/deltaY
            yIntEq2 = (slopeEq2 * self.avgPts[2][0]) + self.avgPts[2][1]
            #Calculate the intersection point of Eq1 and Eq2
            xInt = (int)((yIntEq2 - yIntEq1) / (slope - slopeEq2))
            yInt = (int)(slopeEq1 * xInt) + yIntEq1
            #Find the three side lengths
            Q2toQ3 = self.calcDistance(self.avgPts[1], self.avgPts[2])
            Q3toQ4 = self.calcDistacne(self.avgPts[2], self.avgPts[3])
            sharedSide = self.calcDistance(self.avgPts[2], [xInt, yInt])
            #Use trig to calculate angles
            ang1 = math.degrees(math.cos(sharedSide / Q2toQ3))
            ang2 = math.degrees(math.cos(sharedSide / Q3toQ4))

            #FIND THE SECOND TWO ANGLES
            #Eq1 refers to line equation of the line between Quads 1 and 3
            #Eq2 refers to the equation of the perp line between Quad 2
                #and the point of intersection of eq1
            #Calculate the y=mx+b equation of eq1
            deltaY = self.avgPts[2][1] - self.avgPts[0][1]
            deltaX = self.avgPts[2][0] - self.avgPts[0][0]
            slopeEq1 = deltaY/deltaX
            yIntEq1 = slope * self.avgPts[2][0]
            #Calculate the y=mx+b equation of eq2 using point slope
            slopeEq2 = -deltaX/deltaY
            yIntEq2 = (slopeEq2 * self.avgPts[3][0]) + self.avgPts[3][1]
            #Calculate the intersection point of Eq1 and Eq2
            xInt = (int)((yIntEq2 - yIntEq1) / (slope - slopeEq2))
            yInt = (int)(slopeEq1 * xInt) + yIntEq1
            #Find the three side lengths
            Q4toQ1 = self.calcDistance(self.avgPts[1], self.avgPts[2])
            sharedSide = self.calcDistance(self.avgPts[3], [xInt, yInt])
            #Use trig to calculate angles
            ang3 = math.degrees(math.cos(sharedSide / Q3toQ4))
            ang4 = math.degrees(math.cos(sharedSide / Q4toQ1))

            #Check if the angles' sum are around 240 degrees
            if abs((ang1 + ang2 + ang3 + ang4) - 240) != 10:
                self.isAG2 = False



    def doEverything(self):
        self.calcCentroid()
        self.seperateIntoQuads()
        self.seperateQuadsIntoIvO()
        self.findAvgs()
        self.amIG2()
        print(self.isAG2)

    #doEverything()


