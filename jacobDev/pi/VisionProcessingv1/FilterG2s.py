import cv2

from G2Class import G2Class

class FilterG2s:

    def __init__(self):
        self.G2s = []
        self.theTrueG2 = []

    def addG2(self, cnt, approx, approxID):
        g2 = G2Class(cnt, approx, approxID)
        self.G2s.append(g2)

    def findTheG2(self):
        for g2 in self.G2s:
            g2.doEverything()
        for g2 in self.G2s:
            if g2.isAG2:
                self.theTrueG2.append(g2)
        if len(self.theTrueG2) == 1:
            print("ONLY ONE G2 FOUND")  
            return self.theTrueG2[0]

        
