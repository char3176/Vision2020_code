import cv2 as cv

class G2Class:

    #img = cv.imread('test.jpg')

	approxPts = []
    self.centroid = []

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

    def __init__(self, approx):
        if len(approx) == 4 or 8:
            self.approxPts = approx
	
	self.approxPts = []
	self.centroid = []

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


    def calcCentroid(self):
        #Compute the centroid of the contour
        M = cv.Moments(approxPts)
        cX = int(M["m10"], M["m00"])
        cY = int(M["m01"], M["m00"])
        self.centroid = [cX, cY]

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
            avgPts.append((int)(RTpts[0] + RTpts[1])/2)
            avgPts.append((int)(LTpts[0] + LTpts[1])/2)
            avgPts.append((int)(LBpts[0] + LBpts[1])/2)
            avgPts.append((int)(RBpts[0] + RBpts[1])/2)
        else:
            #If 1 point per quadrant, make the average our only point
            avgPts.append(RTpts)
            avgPts.append(LTpts)
            avgPts.append(LBpts)
            avgPts.appemd(RBpts)

    def doEverything():
        self.calcCentroid()
        seperateIntoQuads()
        seperateQuadsIntoIvO()
        findAvgs()
        print("Done!")

    doEverything()

        
