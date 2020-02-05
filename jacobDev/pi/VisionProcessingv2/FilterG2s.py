import cv2

from G2Class import G2Class

class FilterG2s:

    def __init__(self):
        self.G2s = []
        self.theOneTrueG2 = []

    def addG2(self, cnt, approx, approxID, frame):
        g2 = G2Class(cnt, approx, approxID,frame)
        #print(g2.newframe)
        self.G2s.append(g2)

    def findTheOneTrueG2(self):
        for g2 in self.G2s:
            g2.doEverything()
        for g2 in self.G2s:
            if g2.isAG2:
                self.theOneTrueG2.append(g2)
        if len(self.theOneTrueG2) == 1:
            return self.theOneTrueG2[0]


