import numpy as np
import cv2 as cv
import sys
from imutils.video import VideoStream
import time
import picamera
import imutils
import argparse




'''
THIS is v1 (scroll down for v2)

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
        return self.after


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



THIS IS v2
'''

import cv2 as cv
import numpy as np


class CHclass:

    def __init__(self, img, scale):
        # ADJUST these variables for different results
        # self.coverageX is how far the crosshair extends from center horizontally, self.coverageY is vertically
        self.coverageX = 150
        self.coverageY = 150
        # self.scope is how far the farthest graduation is out from the center, logically is <= both coverage values
        self.scope = 100
        # self.gradDevi is how far each graduation deviates from the center
        # a value of 1 is the distance out of self.scope, while .5 is half that distance
        # the first entry is the circle radius, and each entry is an additional graduation
        self.gradDevi = [.25, .5, .75, 1]
        # other visual variables
        # Crosshair thickness & color
        self.CrThick = 2
        self.CrCol = [255, 40, 0]
        # circle
        self.cirThick = 3
        self.cirCol = [0, 0, 255]
        # graduations
        self.gradLen = 20
        # how much bigger each graduation is than the last
        self.gradInc = 15
        self.gradThick = 2
        self.gradCol = [255, 260, 15]
        # bar (thickness only)
        self.barThick = 10

        # LEAVE these alone, they just manipulate the adjustable ones
        self.img = img
        self.scale = scale
        self.width = len(self.img[1])
        self.height = len(self.img[0])
        self.center = [int(self.width / 2), int(self.height / 2)]
        # multiplies all important variables by the entered scale ( if the scale < 1, values get smaller, and they get bigger if the scale < 1 )
        self.coverageX = int(self.coverageX * self.scale)
        self.coverageY  = int(self.coverageY * self.scale)
        self.scope = int(self.scope * self.scale)
        self.gradLen = int(self.gradLen * self.scale)
        self.gradLenO = self.gradLen
        self.gradInc = int(self.gradInc * self.scale)
        self.cirRad = int(self.gradDevi[0] * self.scope)
        del self.gradDevi[0]
        self.gradDiff = []
        for deviation in self.gradDevi:
            # do not also multiply deviation by self.scale because self.scope has already done that and takes care of the difference
            deviation = int(deviation * self.scope)
            self.gradDiff += [deviation]


    # draws the crosshair and circle on the image
    def drawCross(self):
        self.after = cv.line(self.img, ((self.center[0] - self.coverageX), self.center[1]), ((self.center[0] + self.coverageX), self.center[1]),
            (self.CrCol[0], self.CrCol[1], self.CrCol[2]), self.CrThick)
        self.after = cv.line(self.after, (self.center[0], (self.center[1] - self.coverageY)), (self.center[0], (self.center[1] + self.coverageY)),
            (self.CrCol[0], self.CrCol[1], self.CrCol[2]), self.CrThick)
        self.after = cv.circle(self.after, (self.center[0], self.center[1]), self.cirRad, (self.cirCol[0], self.cirCol[1], self.cirCol[2]), self.cirThick)
        return self.after


    # draws graduations on the vertical crosshair above and below the circle
    # the number of graduations is dictated by the number of entries in self.gradDevi
    # the deviation from the center is dictated by the values in self.gradDevi
    def drawGrads(self):
        # draws the graduations below the circle
        for diff in self.gradDiff:
            self.after = cv.line(self.after, ((self.center[0] - self.gradLen), (self.center[1] + diff)), ((self.center[0] + self.gradLen),
                (self.center[1] + diff)), (self.gradCol[0], self.gradCol[1], self.gradCol[2]), self.gradThick)
            # each += makes the next graduation out a little bigger (by the value of self.gradInc
            self.gradLen += self.gradInc
        # resets self.gradLen to its original before doing the ones above the circle
        self.gradLen = self.gradLenO
        for diff in self.gradDiff:
            self.after = cv.line(self.after, ((self.center[0] - self.gradLen), (self.center[1] - diff)), ((self.center[0] + self.gradLen),
                (self.center[1] - diff)), (self.gradCol[0], self.gradCol[1], self.gradCol[2]), self.gradThick)
            self.gradLen += self.gradInc
        # used to undo the final increase of self.gradLen because it is unnecessary, since there are no further graduations being created
        # self.gradLen is not reset to original because we use this to determine the sizes of the bars in drawBars()
        self.gradLen -= self.gradInc
        return self.after


    # draws two thick bars on the horizontal crosshair, beginning at the ending y-value of the biggest graduation and going out to end of self.coverage
    def drawBars(self):
        self.after = cv.line(self.after, ((self.center[0] - self.coverageX), self.center[1]), ((self.center[0] - self.gradLen), self.center[1]),
            (self.gradCol[0], self.gradCol[1], self.gradCol[2]), self.barThick)
        self.after = cv.line(self.after, ((self.center[0] + self.coverageX), self.center[1]), ((self.center[0] + self.gradLen), self.center[1]),
            (self.gradCol[0], self.gradCol[1], self.gradCol[2]), self.barThick)
        return self.after


def main(argv=None):
  ap= argparse.ArgumentParser()
  ap.add_argument("-p", "--picamera", type=int, default=1, help="whether or not the Raspi camera should be used")
  args = vars(ap.parse_args())
#  vs = VideoStream(usePiCamera=args["picamera"] > 0, resolution=(320, 240),framerate=60).start()
  vs = VideoStream(usePiCamera=args["picamera"] > 0, resolution=(640, 480),framerate=60).start()
#  vs = VideoStream(usePiCamera=args["picamera"] > 0, resolution=(640, 480),framerate=90).start()
#  vs = VideoStream(usePiCamera=args["picamera"] > 0, resolution=(1280, 720),framerate=60).start()
#  vs = VideoStream(usePiCamera=args["picamera"] > 0, resolution=(1640, 922),framerate=40).start()
#  vs = VideoStream(usePiCamera=args["picamera"] > 0, resolution=(1920, 1080),framerate=30).start()
#  vs = VideoStream(usePiCamera=args["picamera"] > 0, resolution=(1640, 1232),framerate=40).start()
#  vs = VideoStream(usePiCamera=args["picamera"] > 0, resolution=(3280, 2464),framerate=15).start()
  time.sleep(2.0)
  vs.camera.brightness = 30
  vs.camera.contrast = 100
  vs.camera.saturation = 100

  #DA MASTA LOOP
  while True:
          #Grab the frame
          frame = vs.read()
          #frame = imutils.resize(frame, width=320)
          #frame = imutils.rotate(frame, 90)

          #with picamera.array.PiRGBArray(camera) as stream:
              #camera.capture(stream, format="bgr")
              #frame = stream.array

          #img = np.zeros((600, 600, 3), np.uint8)
          img = frame.copy()
          scale = 1
          CHover = CHclass(img, scale)
          imgCross = CHover.drawCross()
          imgGrads = CHover.drawGrads()
          imgBars = CHover.drawBars()
          cv.imshow("CH v2", imgBars)

          #frame = VisionProcessing(frame)
#          cv.imshow("VP", frame)
          key = cv.waitKey(1) & 0xFF

          if key == ord("q"):
              break

  cv.destroyAllWindows()
  vs.stop()


if __name__ == "__main__":
  main(sys.argv)
