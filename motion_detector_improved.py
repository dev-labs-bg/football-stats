# USAGE
# python motion_detector.py
# python motion_detector.py --video 'video_file_name'

# import the necessary packages
import argparse
import datetime
import imutils
import time
import cv2
import numpy as np
from coordinate_transform import windowToFieldCoordinates

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
ap.add_argument("-a", "--min-area", type=int, default=5000, help="minimum area size")
args = vars(ap.parse_args())

# if the video argument is None, then we are reading from webcam
if args.get("video", None) is None:
	camera = cv2.VideoCapture(0)
	time.sleep(0.25)

# otherwise, we are reading from a video file
else:
	camera = cv2.VideoCapture(args["video"])

fgbg = cv2.BackgroundSubtractorMOG2()

# loop over the frames of the video
while True:
	# grab the current frame and initialize the occupied/unoccupied
	# text
	(grabbed, frame) = camera.read()

	# if the frame could not be grabbed, then we have reached the end
	# of the video
	if not grabbed:
		break

	# resize the frame, convert it to grayscale, and blur it
	frame = imutils.resize(frame, width=600)

	fgmask = fgbg.apply(frame, learningRate=0.02)

	fgmask = cv2.GaussianBlur(fgmask, (21, 21), 0)
	thresh = cv2.threshold(fgmask, 25, 255, cv2.THRESH_BINARY)[1]
	thresh = cv2.dilate(thresh, None, iterations=3)

	(contours, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	# loop over the contours
	for contour in contours:
		# if the contour is too small, ignore it
		if cv2.contourArea(contour) < args["min_area"]:
			continue

		# compute the bounding box for the contour, draw it on the frame,
		# and update the text
		(x, y, w, h) = cv2.boundingRect(contour)
		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

		basepoint = ((x + (w/2)), (y + h))
		cv2.circle(frame, basepoint, 3, (0,0,255), 2)

	# perspective coordinates
	(xa1, ya1) = (225, 150)
	(xa2, ya2) = (490, 150)
	(xa3, ya3) = (595, 335)
	(xa4, ya4) = (60, 335)

	# draw perspective filed, line by line
	cv2.line(frame, (xa1, ya1), (xa2, ya2), (0, 255, 0), 2)
	cv2.line(frame, (xa2, ya2), (xa3, ya3), (0, 255, 0), 2)
	cv2.line(frame, (xa3, ya3), (xa4, ya4), (0, 255, 0), 2)
	cv2.line(frame, (xa4, ya4), (xa1, ya1), (0, 255, 0), 2)

	# Create a black image
	field = np.zeros((384,256,3), np.uint8)

	# bird-eye rectangle coordinates
	(xb1, yb1) = (20, 20)
	(xb2, yb2) = (230, 20)
	(xb3, yb3) = (230, 350)
	(xb4, yb4) = (20, 350)

	# draw bird-eye filed, line by line
	cv2.line(field, (xb1, yb1), (xb2, yb2), (0, 255, 0), 2)
	cv2.line(field, (xb2, yb2), (xb3, yb3), (0, 255, 0), 2)
	cv2.line(field, (xb3, yb3), (xb4, yb4), (0, 255, 0), 2)
	cv2.line(field, (xb4, yb4), (xb1, yb1), (0, 255, 0), 2)

	# get the basepoint original coordinates
	(xa, ya) = basepoint

	# get bird-eye field dimensions
	resultWidth = xb2 - xb1
	resultHeight = yb3 - yb1
	
	resultCoord = windowToFieldCoordinates(xa, ya, xa1, ya1, xa2, ya2, xa3, ya3, xa4, ya4, resultWidth, resultHeight)
	xb = xb1 + int(resultCoord[0])
	yb = yb1 + int(resultCoord[1])

	cv2.circle(field, (xb, yb), 3, (0,0,255), 2)

	cv2.imshow('frame',frame)	
	# cv2.imshow('thresh',thresh)
	cv2.imshow('field',field)

	# wait for key press
	key = cv2.waitKey(1) & 0xFF

	# if the `q` key is pressed, break from the lop
	if key == ord("q"):
		break

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()