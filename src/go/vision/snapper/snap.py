#!/usr/bin/env python3

from time import sleep
import cv2

class Snapper:
    def __init__(self):
        self.cam = cv2.VideoCapture("http://146.244.98.34:5000/video_feed")
        if not self.cam.isOpened():
            raise Exception("Could not open video stream.")

    def get_frame(self):
            #TODO fix imports for more modularity
            CURRENT_FRAME = "/home/WorkingPC/WorkingDir/src/go/vision/snapper/current_frame.jpg"
            ret, frame = self.cam.read()
            if not ret:
                raise Exception("Failed to read frame from stream.")
            if frame is not None:
                cv2.imwrite(CURRENT_FRAME, frame)

if __name__ == "__main__":
    snapper = Snapper()
    while True:
         snapper.get_frame()
         sleep(.001)