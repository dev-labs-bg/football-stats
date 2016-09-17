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

# Mouse class definition
class Mouse:
	x = 0
	y = 0
	clicked = False

	def left_click(self,event,x,y,flags,param):
		if event == cv2.EVENT_LBUTTONDOWN:
			mouse.x = x
			mouse.y = y
			mouse.clicked = True

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

# init frame_count and create mouse object
frame_count = 0
mouse = Mouse()

# get BackgroundSubtractor object
fgbg = cv2.BackgroundSubtractorMOG2()

# loop over the frames of the video
while True:
	# grab the current frames
	(grabbed, frame) = camera.read()

	# if the frame could not be grabbed, then end is reached
	if not grabbed:
		break

	# increase frame count
	frame_count += 1

	# resize the frame, to lessen the burden on CPU
	frame = imutils.resize(frame, width=800)

	# freeze first frame util user provides the area of the field
	# (4 points should be given by mouse clicks)
	if frame_count == 1:
		cv2.imshow('frame',frame)	
		cv2.setMouseCallback('frame', mouse.left_click)
		i = 0
		coords = []
		while i < 4:
			i += 1
			mouse.x = 0
			mouse.y = 0
			mouse.clicked = False
			while mouse.clicked == False:
				# wait for key press
				key = cv2.waitKey(1) & 0xFF
			coords.append((mouse.x, mouse.y))

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
	(xa1, ya1) = coords[0]
	(xa2, ya2) = coords[1]
	(xa3, ya3) = coords[2]
	(xa4, ya4) = coords[3]

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