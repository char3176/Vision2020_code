import cv2

from G2Class import G2Class

class FilterG2s:

    def __init__(self):
        self.G2s = []
        self.theTrueG2 = []

    def addG2(self, cnt, approx, approxID):
        g2 = G2Class(cnt, approx, approxID):
        self.G2s += g2

    def findTheG2(self):
        for g2 in G2s:
            g2.doEverything()
        for g2 in G2s:
            if G2s[g2].isAG2:
                self.theTrueG2 += g2
        if len(theTrueG2) == 1:
            return theTrueG2[0]     

        
