import numpy as np
import cv2 as cv

class CHclass:

    def __init__(self, img):
        self.img = img
        self.height = len(self.img[0])
        self.width = len(self.img[1])
        self.center = [int(self.width / 2), int(self.height / 2)]
        self.final = None
        # self.coverage is how far the crosshair extends out from the center point
        self.coverage = int(150)
        # self.range is how far the farthest graduation is from the center point
        self.range = 100
        self.gradDeviate = [int(self.range * .5), int(self.range * .75), int(self.range)]
        self.gradSize = 20
        

    # draws the crosshair on the image and the circle in the middle
    def drawCrosshair(self):
        self.after = cv.line(self.img, ((self.center[0] - self.coverage), self.center[1]), ((self.center[0] + self.coverage), self.center[1]), (255, 95, 0), 2)
        self.after = cv.line(self.after, (self.center[0], (self.center[1] - self.coverage)), (self.center[0], (self.center[1] + self.coverage)), (255, 95, 0), 2)
        self.after = cv.circle(self.after, (self.center[0], self.center[1]), int(self.range * .25), (0, 0, 255), 4)
        return self.final


    # draws graduations along the vertical crosshair
    def drawGraduations(self):
        # draws the graduations below the circle
        for gradDist in self.gradDeviate:
            self.after = cv.line(self.after, ((self.center[0] - self.gradSize), (self.center[1] + gradDist)), ((self.center[0] + self.gradSize),
                (self.center[1] + gradDist)), (255, 180, 20), 2)
            # each += makes the next graduation out a little bigger
            self.gradSize += 20
        # resets gradSize to its original 20 before doing the ones above the circle
        self.gradSize = 20
        for gradDist in self.gradDeviate:
            self.after = cv.line(self.after, ((self.center[0] - self.gradSize), (self.center[1] - gradDist)), ((self.center[0] + self.gradSize),
                (self.center[1] - gradDist)), (255, 180, 20), 2)
            self.gradSize += 20
        self.gradSize -= 20
        return self.after


    # draws two thick bars on the horizontal crosshair, beginning at the ending y-value of the biggest graduation and going out to end of self.coverage
    def drawCentering(self):
        self.after = cv.line(self.after, ((self.center[0] - self.coverage), self.center[1]), ((self.center[0] - self.gradSize), self.center[1]), (255, 180, 20), 10)
        self.after = cv.line(self.after, ((self.center[0] + self.coverage), self.center[1]), ((self.center[0] + self.gradSize), self.center[1]), (255, 180, 20), 10)
        return self.after


#DA MASTA SCRIPT (cause it's not a loop)
img = np.zeros((600, 600, 3), np.uint8)
#img = cv.imread("20200117-202124_16-100-74_2.jpg")
CHtest = CHclass(img)
imgCrosshair = CHtest.drawCrosshair()
imgGraduations = CHtest.drawGraduations()
imgCentering = CHtest.drawCentering()
cv.imshow("Blank", imgCentering)
