import numpy as np
import cv2 as cv

class CHclass:

    def __init__(self, img):
        self.img = img
        self.height = len(self.img[0])
        self.width = len(self.img[1])
        self.center = [int(self.width / 2), int(self.height / 2)]
        self.final = None
        
    
    def drawCrosshair(self):
        self.final = cv.circle(self.img, (self.center[0], self.center[1]), 51, (0, 0, 255), 4)
        self.final = cv.line(self.final, ((self.center[0] - 150), self.center[1]), ((self.center[0] + 150), self.center[1]), (255, 95, 0), 2)
        self.final = cv.line(self.final, (self.center[0], (self.center[1] - 150)), (self.center[0], (self.center[1] + 150)), (255, 95, 0), 2)
        return self.final
        

#DA MASTA SCRIPT (cause it's not a loop)
img = np.zeros((657, 597, 3), np.uint8)
#img = cv.imread("20200117-202124_16-100-74_2.jpg")
CHtest = CHclass(img)
CHfinal = CHtest.drawCrosshair()
cv.imshow("Blank", CHfinal)
