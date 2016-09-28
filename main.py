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
from lib.coordinate_transform import windowToFieldCoordinates
from lib.average_coordinates import getRunningAverageCoordinates
from lib.mouse import Mouse

# Mouse class definition
# class Mouse:
# 	x = 0
# 	y = 0
# 	clicked = False

# 	def left_click(self,event,x,y,flags,param):
# 		if event == cv2.EVENT_LBUTTONDOWN:
# 			mouse.x = x
# 			mouse.y = y
# 			mouse.clicked = True

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

# get bird-eye field dimensions
resultWidth = 280#xb2 - xb1
resultHeight = 334#yb3 - yb1
padding = 20

# Create a black image
field = np.zeros((resultHeight + padding*2,resultWidth + padding*2,3), np.uint8)

# bird-eye rectangle coordinates
(xb1, yb1) = (padding, padding)
(xb2, yb2) = (padding + resultWidth, padding)
(xb3, yb3) = (padding + resultWidth, padding + resultHeight)
(xb4, yb4) = (padding, padding + resultHeight)

# draw bird-eye filed, line by line
cv2.line(field, (xb1, yb1), (xb2, yb2), (0, 255, 0), 2)
cv2.line(field, (xb2, yb2), (xb3, yb3), (0, 255, 0), 2)
cv2.line(field, (xb3, yb3), (xb4, yb4), (0, 255, 0), 2)
cv2.line(field, (xb4, yb4), (xb1, yb1), (0, 255, 0), 2)

# loop over the frames of the video
while True:
	# grab the current frames
	(grabbed, frame) = camera.read()

	# if the frame could not be grabbed, then end is reached
	if not grabbed:
		break

	# resize the frame, to lessen the burden on CPU
	frame = imutils.resize(frame, width=800)

	# increase frame count
	frame_count += 1

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
		basepoint = ((x + (w/2)), (y + h))
		resultCoord = windowToFieldCoordinates(basepoint[0], basepoint[1], xa1, ya1, xa2, ya2, xa3, ya3, xa4, ya4, resultWidth, resultHeight)
		resX = int(resultCoord[0])
		resY = int(resultCoord[1])

		if resX < 0 or resX > resultWidth or resY < 0 or resY > resultHeight:
			print "Skipped a contour, not a cool contour"
		else:
			cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
			cv2.circle(frame, basepoint, 3, (0, 0, 255), 2)

			resultCoord = getRunningAverageCoordinates(resultCoord)
			xb = xb1 + int(resultCoord[0])
			yb = yb1 + int(resultCoord[1])

			# draw overlayed opacity circle every 10 frames
			if frame_count % 5 == 0:
				overlay = field.copy()
				cv2.circle(overlay, (xb, yb), 0, (0,0,255), 15)
				alpha = 0.25
				cv2.addWeighted(overlay, alpha, field, 1 - alpha, 0, field)

	cv2.imshow('frame',frame)
	def clickDebug(event,x,y,flags,param):
		resultCoord = windowToFieldCoordinates(x, y, xa1, ya1, xa2, ya2, xa3, ya3, xa4, ya4, resultWidth, resultHeight)
		print "Coordinates to real coordinates", resultCoord
	# UNCOMMENT IF YOU WANT TO DEBUG
	# cv2.setMouseCallback('frame', clickDebug)

	cv2.imshow('thresh',thresh)
	cv2.imshow('field',field)

	# wait for key press
	key = cv2.waitKey(1) & 0xFF

	# if the `q` key is pressed, break from the lop
	if key == ord("q"):
		break

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()