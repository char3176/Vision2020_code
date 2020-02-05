import cv2
import imutils
import numpy as np
import argparse
from collections import deque

from ballPipeline import BallPipeline
from ballClass import BallClass
from manyTo1B import ManyTo1B
from newBallPipeline import NewBallPipeline

img = cv2.imread("ball2.jpg")
bp = BallPipeline()
#bp = NewBallPipeline()
cnts = bp.process(img)
mb = ManyTo1B(cnts)
mb.coord()


