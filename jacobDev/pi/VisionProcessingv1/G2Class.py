import cv2 as cv
import math

class G2Class:

    isAG2 = False
    
    approxPts = []
    centroid = []

    # Quadrant Points
    RTpts = []
    LTpts = []
    LBpts = []
    RBpts = []

    #Outer Points
    outerPts = []
    #Inner Points
    innerPts = []
    #Averages
    avgPts = []

    #Vision Tape Constants
    LTtoRTLen = 39.25
    #Average between inner and outer lengths
    SideLen = (17.5 + 19.625) / 2
    

    def __init__(self, approx):
        if len(self.approx) == 4 or 8:
            approxPts = self.approx

    def calcCentroid():
        #Compute the centroid of the contour
        M = cv.Moments(approxPts)
        cX = int(M["m10"], M["m00"])
        cY = int(M["m01"], M["m00"])
        centroid = [cX, cY]

    def seperateIntoQuads():
        for pnt in approxPts:
            if pnt[0] > cX:
                if pnt[1] < cY:
                    RTpts.append(pnt)
                else:
                    RBpts.append(pnt)
            else:
                if pnt[1] < cY:
                    LTpts.append(pnt)
                else:
                    LBpts.append(pnt)

    def seperateQuadsIntoIvO():
        if len(approxPts) == 8:
            #Quadrant 1: RT
            if RTpts[0][0] > RTpts[1][0]:
                innerPts.append(RTpts[0])
                outerPts.append(RTpts[1])
            else:
                innerPts.append(RTpts[1])
                outerPts.append(RTpts[0])

            #Quadrant 2: LT
            if LTpts[0][0] > LTpts[1][0]:
                innerPts.append(LTpts[0])
                outerPts.append(LTpts[1])
            else:
                innerPts.append(LTpts[1])
                outerPts.append(LTpts[0])

            #Quadrant 3: LB
            if LBpts[0][0] > LBpts[1][0]:
                innerPts.append(LBpts[0])
                outerPts.append(LBpts[1])
            else:
                innerPts.append(LBpts[1])
                outerPts.append(LBpts[0])

            #Quadrant 4: RB
            if RBpts[0][0] > RBpts[1][0]:
                innerPts.append(RBpts[0])
                outerPts.append(RBpts[1])
            else:
                innerPts.append(RBpts[1])
                outerPts.append(RBpts[0])

    def findAvgs():
        if len(RTpts) == 2:
            #Average the two points in each quadrant
            XCoord = (int)(RTpts[0][0] + RTpts[1][0])/2
            YCoord = (int)(RTpts[0][1] + RTpts[1][1])/2
            avgPts.append([XCoord, YCoord])
            XCoord = (int)(LTpts[0][0] + LTpts[1][0])/2
            YCoord = (int)(LTpts[0][1] + LTpts[1][1])/2
            avgPts.append([XCoord, YCoord])
            XCoord = (int)(LBpts[0][0] + LBpts[1][0])/2
            YCoord = (int)(LBpts[0][1] + LBpts[1][1])/2
            avgPts.append([XCoord, YCoord])
            XCoord = (int)(RBpts[0][0] + RBpts[1][0])/2
            YCoord = (int)(RBpts[0][1] + RBpts[1][1])/2
            avgPts.append([XCoord, YCoord])
        else:
            #If 1 point per quadrant, make the average our only point
            avgPts.append(RTpts)
            avgPts.append(LTpts)
            avgPts.append(LBpts)
            avgPts.appemd(RBpts)

    def calcDistance(point1, point2):
        xDiff = point1[0] - point2[0]
        yDiff = point1[1] - point2[1]
        dist = math.sqrt((xDiff * xDiff) + (yDiff * yDiff))
        return dist

    def amIG2():
        #FIND THE FIRST TWO ANGLES
        #Find longest side using the distance formula
        LTtoRTImgDist = calcDistance(avgPts[1], avgPts[3])
        #Find shortest side using the distance formula
        xDiff = avgPts[2][0] - avgPts[3][0]
        yDiff = avgPts[2][1] - avgPts[3][1]
        LBtoRBImgDist = math.sqrt((xDiff * xDiff) + (yDiff * yDiff))
        #Find the ratio
        distRatioImg = LTtoRTImgDist/LBtoRBImgDist
        distRatioReal = LTtoRTLen / sideLen
        #If ratios aren't similar, we're not looking at a G2
        if abs(distRatioImg - distRatioReal) < 0.1:            
           isAG2 = True
           
        #Go to next text if it passed the first
        if isAG2:
            #Eq1 refers to line equation of the line between Quads 2 and 4
            #Eq2 refers to the equation of the perp line between Quad 3
                #and the point of intersection of eq1
            #Calculate the y=mx+b equation of eq1
            deltaY = avgPts[3][1] - avgPts[1][1]
            deltaX = avgPts[3][0] - avgPts[1][0]
            slopeEq1 = deltaY/deltaX
            yIntEq1 = slope * avgPts[1][0]
            #Calculate the y=mx+b equation of eq2 using point slope
            slopeEq2 = -deltaX/deltaY
            yIntEq2 = (slopeEq2 * avgPts[2][0]) + avgPts[2][1]
            #Calculate the intersection point of Eq1 and Eq2
            xInt = (int)((yIntEq2 - yIntEq1) / (slope - slopeEq2))
            yInt = (int)(slopeEq1 * xInt) + yIntEq1
            #Find the three side lengths
            Q2toQ3 = calcDistance(avgPts[1], avgPts[2])
            Q3toQ4 = calcDistacne(avgPts[2], avgPts[3])
            sharedSide = calcDistance(avgPts[2], [xInt, yInt])
            #Use trig to calculate angles
            ang1 = math.degrees(math.cos(sharedSide / Q2toQ3))
            ang2 = math.degrees(math.cos(sharedSide / Q3toQ4))

            #FIND THE SECOND TWO ANGLES
            #Eq1 refers to line equation of the line between Quads 1 and 3
            #Eq2 refers to the equation of the perp line between Quad 2
                #and the point of intersection of eq1
            #Calculate the y=mx+b equation of eq1
            deltaY = avgPts[2][1] - avgPts[0][1]
            deltaX = avgPts[2][0] - avgPts[0][0]
            slopeEq1 = deltaY/deltaX
            yIntEq1 = slope * avgPts[2][0]
            #Calculate the y=mx+b equation of eq2 using point slope
            slopeEq2 = -deltaX/deltaY
            yIntEq2 = (slopeEq2 * avgPts[3][0]) + avgPts[3][1]
            #Calculate the intersection point of Eq1 and Eq2
            xInt = (int)((yIntEq2 - yIntEq1) / (slope - slopeEq2))
            yInt = (int)(slopeEq1 * xInt) + yIntEq1
            #Find the three side lengths
            Q4toQ1 = calcDistance(avgPts[1], avgPts[2])
            sharedSide = calcDistance(avgPts[3], [xInt, yInt])
            #Use trig to calculate angles
            ang3 = math.degrees(math.cos(sharedSide / Q3toQ4))
            ang4 = math.degrees(math.cos(sharedSide / Q4toQ1))

            #Check if the angles' sum are around 240 degrees
            if abs((ang1 + ang2 + ang3 + ang4) - 240) != 10:
                isAG2 = False

        return isAG2


    def doEverything():
        calcCentroid()
        seperateIntoQuads()
        seperateQuadsIntoIvO()
        findAvgs()
        amIG2()
        print(isAG2)

    doEverything()

        
