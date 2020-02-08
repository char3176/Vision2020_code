import numpy as np
import cv2 as cv
import sys
from imutils.video import VideoStream
import time
import picamera
import imutils
import argparse




'''
THIS is v0 (scroll down for others, along with current)

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



Below was v1, currently v1.3
'''

class CHclass:

    def __init__(self, img, scale, inROF):
        # ADJUST these variables for different results
        # self.coverageX is how far the crosshair extends from center horizontally, self.coverageY is vertically
        self.coverageX = 100
        self.coverageY = 100
        # self.scope is how far the farthest graduation is out from the center, logically is <= both coverage values
        self.scope = 80
        # self.gradDevi is how far each graduation deviates from the center
        # a value of 1 is the distance out of self.scope, while .5 is half that distance
        # the first entry is the circle radius, and each entry is an additional graduation
        self.gradDevi = [.25, .5, .75, 1]
        # other visual variables
        # Crosshair thickness & color
        self.CrThick = 2
        self.CrCol = [255, 40, 0]
        # circle
        self.cirThick = 2
        self.cirColOut = [0, 0, 255]
        self.cirColIn = [215, 70, 255]
        # graduations
        self.gradLen = 15
        # how much bigger each graduation is than the last
        self.gradInc = 10
        self.gradThick = 2
        self.gradCol = [255, 255, 15]
        # bar
        self.barColIn = [215, 70, 255]
        self.barColOut = [255, 255, 15]
        self.barThick = 3

        # LEAVE these alone, they just manipulate the adjustable ones
        self.img = img
        # the scale set by the user and the resolution of the image determine the overall scale of the crosshair
        # The 600 seems to be the optimal default resolution scale number, but it can be refined later if needed
        # That 600 is not a variable because having two scale variables seems unnecessary
        self.scale = scale * (len(self.img) / 600)
        self.width = len(self.img[0])
        self.height = len(self.img)
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
        self.inROF = inROF
        if self.inROF:
            self.cirCol = self.cirColIn
            self.barCol = self.barColIn
        else:
            self.cirCol = self.cirColOut
            self.barCol = self.barColOut


    # draws the crosshair and circle on the image
    # There are now four lines (two vertical and two horizontal) so that the inside of the circle is empty
    def drawCross(self):
        self.after = cv.line(self.img, ((self.center[0] - self.coverageX), self.center[1]), ((self.center[0] - self.cirRad), self.center[1]),
            (self.CrCol[0], self.CrCol[1], self.CrCol[2]), self.CrThick)
        self.after = cv.line(self.after, ((self.center[0] + self.coverageX), self.center[1]), ((self.center[0] + self.cirRad), self.center[1]),
            (self.CrCol[0], self.CrCol[1], self.CrCol[2]), self.CrThick)
        self.after = cv.line(self.after, (self.center[0], (self.center[1] - self.coverageY)), (self.center[0], (self.center[1] - self.cirRad)),
            (self.CrCol[0], self.CrCol[1], self.CrCol[2]), self.CrThick)
        self.after = cv.line(self.after, (self.center[0], (self.center[1] + self.coverageY)), (self.center[0], (self.center[1] + self.cirRad)),
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
            # each += makes the next graduation out a little bigger (by the value of self.gradInc)
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
    # the bars are actually rectangles because opencv rounds out lines, which made the thick bars look too far inside when drawn as lines
    def drawBars(self):
        self.after = cv.rectangle(self.after, ((self.center[0] - self.coverageX), (self.center[1] - self.barThick)), ((self.center[0] - self.gradLen),
           (self.center[1] + self.barThick)), (self.barCol[0], self.barCol[1], self.barCol[2]), -1)
        self.after = cv.rectangle(self.after, ((self.center[0] + self.coverageX), (self.center[1] - self.barThick)), ((self.center[0] + self.gradLen),
           (self.center[1] + self.barThick)), (self.barCol[0], self.barCol[1], self.barCol[2]), -1)
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

          # variables to be passed in
          # toggle turns the crosshair on or off
          toggle = True
          # inROF will be passed from Jake's G2class to see if the goal is in the center of the image and therefore it's safe to shoot
          # it it's safe to shoot, the colors of the circle and bars on the chrosshair will change
          inROF = True
          # scale scales the whole crosshair (value <1 makes it smaller, value >1 makes it bigger)
          scale = 1

          if toggle:
            CHover = CHclass(img, scale, inROF)
            imgCross = CHover.drawCross()
            imgGrads = CHover.drawGrads()
            imgBars = CHover.drawBars()
            cv.imshow("Crosshair (v1.3)", imgBars)
          else:
            cv.imshow("Crosshair (v1.3)", img)


          #frame = VisionProcessing(frame)
#          cv.imshow("VP", frame)
          key = cv.waitKey(1) & 0xFF

          if key == ord("q"):
              break

  cv.destroyAllWindows()
  vs.stop()


if __name__ == "__main__":
  main(sys.argv)
