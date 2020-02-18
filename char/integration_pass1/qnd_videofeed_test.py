# Import the camera server
from cscore import CameraServer

# Import OpenCV and NumPy
import cv2
import numpy as np
from imutils.video import VideoStream


#vs = VideoStream(usePiCamera=args["picamera"] > 0, resolution=(3280, 2464),framerate=15).start()

def main():
    #vs = VideoStream(usePiCamera=args["picamera"] > 0, resolution=(320, 240),framerate=60).start()
    #vs = VideoStream(usePiCamera=args["picamera"] > 0, resolution=(640, 480),framerate=60).start()
    vs = VideoStream(usePiCamera=args["picamera"] > 0, resolution=(640, 480),framerate=90).start()
    #vs = VideoStream(usePiCamera=args["picamera"] > 0, resolution=(1280, 720),framerate=60).start()
    #vs = VideoStream(usePiCamera=args["picamera"] > 0, resolution=(1640, 922),framerate=40).start()
    #vs = VideoStream(usePiCamera=args["picamera"] > 0, resolution=(1920, 1080),framerate=30).start()
    #vs = VideoStream(usePiCamera=args["picamera"] > 0, resolution=(1640, 1232),framerate=40).start()
    time.sleep(2.0)
    vs.camera.brightness = 50
    vs.camera.contrast = 0
    vs.camera.saturation = 0

    cs = CameraServer.getInstance()
    cs.enableLogging()

    # Capture from the first USB Camera on the system
    #camera = cs.startAutomaticCapture()
    #camera.setResolution(320, 240)

    # Get a CvSink. This will capture images from the camera
    cvSink = cs.getVideo()

    # (optional) Setup a CvSource. This will send images back to the Dashboard
    outputStream = cs.putVideo("Name", 320, 240)

    # Allocating new images is very expensive, always try to preallocate
    #img = np.zeros(shape=(240, 320, 3), dtype=np.uint8)

    while True:
        frame = vs.read()
        # Tell the CvSink to grab a frame from the camera and put it
        # in the source image.  If there is an error notify the output.
        #time, frame = cvSink.grabFrame(frame)
        if time == 0:
            # Send the output the error.
            outputStream.notifyError(cvSink.getError());
            # skip the rest of the current iteration
            continue

        #
        # Insert image processing logic here
        #

        # (optional) send some image back to the dashboard
        outputStream.putFrame(frame)

vs.stop()

if __name__ == "__main__":
  main()

