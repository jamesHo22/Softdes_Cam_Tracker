# Code is from https://www.pyimagesearch.com/2018/07/30/opencv-object-tracking/
# USAGE
# python opencv_object_tracking.py
# python opencv_object_tracking.py --video dashcam_boston.mp4 --tracker csrt
# import the necessary packages
from imutils.video import VideoStream
from imutils.video import FPS
import argparse
import imutils
import time
import cv2

class newTracker():
    
    def __init__(self):
        # construct the argument parser and parse the arguments
        ap = argparse.ArgumentParser()
        ap.add_argument("-v", "--video", type=str,
                        help="path to input video file")
        ap.add_argument("-t", "--tracker", type=str, default="kcf",
                        help="OpenCV object tracker type")
        self.args = vars(ap.parse_args())

        # extract the OpenCV version info
        (major, minor) = cv2.__version__.split(".")[:2]

        # if we are using OpenCV 3.2 OR BEFORE, we can use a special factory
        # function to create our object tracker
        if int(major) == 3 and int(minor) < 3:
            self.tracker = cv2.Tracker_create(self.args["tracker"].upper())

        # otherwise, for OpenCV 3.3 OR NEWER, we need to explicity call the
        # approrpiate object tracker constructor:
        else:
            # initialize a dictionary that maps strings to their corresponding
            # OpenCV object tracker implementations
            OPENCV_OBJECT_TRACKERS = {
                "csrt": cv2.TrackerCSRT_create,
                    "kcf": cv2.TrackerKCF_create,
                    "boosting": cv2.TrackerBoosting_create,
                    "mil": cv2.TrackerMIL_create,
                    "tld": cv2.TrackerTLD_create,
                    "medianflow": cv2.TrackerMedianFlow_create,
                    "mosse": cv2.TrackerMOSSE_create
            }

            # grab the appropriate object tracker using our dictionary of
            # OpenCV object tracker objects
            self.tracker = OPENCV_OBJECT_TRACKERS[self.args["tracker"]]()

        # initialize the bounding box coordinates of the object we are going
        # to track
        self.initBB = None

        # if a video path was not supplied, grab the reference to the web cam
        if not self.args.get("video", False):
            print("[INFO] starting video stream...")
            self.vs = VideoStream(src=0).start()
            time.sleep(1.0)

        # otherwise, grab a reference to the video file
        else:
            self.vs = cv2.VideoCapture(self.args["video"])

        # initialize the FPS throughput estimator
        self.fps = None

        # if we are using a webcam, release the pointer
        if not self.args.get("video", False):
            self.vs.stop()

        # otherwise, release the file pointer
        else:
            self.vs.release()

        # close all windows
        cv2.destroyAllWindows()

    def getPosition(self, vs):
        '''
        returns: the x and y position of the tracked object in the frame
        '''
        centerX, centerY = None, None
        # grab the current frame, then handle if we are using a
        # VideoStream or VideoCapture object
        frame = vs.read()
        frame = frame[1] if self.args.get("video", False) else frame

        # check to see if we have reached the end of the stream
        if frame is None:
            # break
            return

        # resize the frame (so we can process it faster) and grab the
        # frame dimensions
        frame = imutils.resize(frame, width=500)
        (H, W) = frame.shape[:2]

        # check to see if we are currently tracking an object
        if self.initBB is not None:
            # grab the new bounding box coordinates of the object
            (success, box) = self.tracker.update(frame)
            

        # check to see if the tracking was a success
            if success:
                (x, y, w, h) = [int(v) for v in box]
                centerX, centerY = int(x + w/2), int(y + h/2)
                cv2.rectangle(frame, (x, y), (x + w, y + h),(0, 255, 0), 2)
                cv2.circle(frame, (centerX, centerY), 1, (0, 255, 0), 1)
            else:
                print('no tracking')
                

            # update the FPS counter
            self.fps.update()
            self.fps.stop()

            # initialize the set of information we'll be displaying on
            # the frame
            info = [
                ("Tracker", self.args["tracker"]),
                    ("Success", "Yes" if success else "No"),
                    ("FPS", "{:.2f}".format(self.fps.fps())),
            ]

            # loop over the info tuples and draw them on our frame
            for (i, (k, v)) in enumerate(info):
                text = "{}: {}".format(k, v)
                cv2.putText(frame, text, (10, H - ((i * 20) + 20)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

        # show the output frame
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF

        # if the 's' key is selected, we are going to "select" a bounding
        # box to track
        if key == ord("s"):
            # select the bounding box of the object we want to track (make
            # sure you press ENTER or SPACE after selecting the ROI)
            self.initBB = cv2.selectROI("Frame", frame, fromCenter=False,
                                showCrosshair=True)

            # start OpenCV object tracker using the supplied bounding box
            # coordinates, then start the FPS throughput estimator as well
            self.tracker.init(frame, self.initBB)
            self.fps = FPS().start()

        # if the `q` key was pressed, break from the loop
        elif key == ord("q"):
            # break
            return
        if centerX == None or centerY == None:
            return 0,0
        else:
            return centerX, centerY
    
        