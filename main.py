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
from lib.mouse import Mouse
from lib.coordinate_transform import windowToFieldCoordinates
from lib.average_coordinates import getRunningAverageCoordinates
from lib.video_source import getVideoSource
from lib.polygon import drawQuadrilateral
from lib.user_interaction import getPerpectiveCoordinates
from lib.user_interaction import leftClickDebug
from lib.fgbg_calculations import getThresholdedFrame
from lib.heatmap import Heatmap

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
ap.add_argument("-fw", "--fieldwidth", type=int, default=280, help="top-view field width")
ap.add_argument("-fh", "--fieldheight", type=int, default=334, help="top-view field height")
args = vars(ap.parse_args())

# get the video source: camera or file
video = getVideoSource(args)

# init frameCount and create mouse object
frameCount = 0
mouse = Mouse()

# get BackgroundSubtractor object
fgbg = cv2.BackgroundSubtractorMOG2()

# get top-view field dimensions
resultWidth = args["fieldwidth"]
resultHeight = args["fieldheight"]
padding = 20

# minimum area of detected object(s)
objectMinArea = resultWidth*0.1 * resultHeight*0.2

# create a black image/frame where the top-view field will be drawn
field = np.zeros((resultHeight + padding*2,resultWidth + padding*2,3), np.uint8)

# top-view rectangle coordinates
(xb1, yb1) = (padding, padding)
(xb2, yb2) = (padding + resultWidth, padding)
(xb3, yb3) = (padding + resultWidth, padding + resultHeight)
(xb4, yb4) = (padding, padding + resultHeight)

# draw the 2D top-view field
drawQuadrilateral(field, xb1, yb1, xb2, yb2, xb3, yb3, xb4, yb4, 0, 255, 0, 2)

# crea heatmap object
heatmap = Heatmap(field, resultWidth, resultHeight)

# loop over the frames of the video
while True:
	# grab the current frame
	(grabbed, frame) = video.read()

	# if the frame could not be grabbed, then end is reached
	if not grabbed:
		break

	# resize the frame, to lessen the burden on CPU
	frame = imutils.resize(frame, width=800)

	# increase frame count
	frameCount += 1

	# freeze first frame util user provides the area of the field
	# (4 points should be given by mouse clicks)
	if frameCount == 1:
		coords = getPerpectiveCoordinates(frame, 'frame', mouse)

	# perspective coordinates
	(xa1, ya1) = coords[0]
	(xa2, ya2) = coords[1]
	(xa3, ya3) = coords[2]
	(xa4, ya4) = coords[3]

	# draw perspective field
	drawQuadrilateral(frame, xa1, ya1, xa2, ya2, xa3, ya3, xa4, ya4, 0, 255, 0, 2)

	# apply color subtractions and calculations to get a black and white frame
	# making it possible for computer to recognize clear contours
	thresh = getThresholdedFrame(fgbg, frame)

	# get the contours of all white regions in the frame
	(contours, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	
	# loop over all contours
	for contour in contours:
		# if the contour is too small, ignore it
		if cv2.contourArea(contour) < objectMinArea:
			continue

		# compute the bounding box for the contour, draw it on the frame
		(x, y, w, h) = cv2.boundingRect(contour)
		basePoint = ((x + (w/2)), (y + h))

		# get the top-view relative coordinates
		(xbRel, ybRel) = heatmap.getPosRelativeCoordinates(basePoint, xa1, ya1, xa2, ya2, xa3, ya3, xa4, ya4)

		if xbRel < 0 or xbRel > resultWidth or ybRel < 0 or ybRel > resultHeight:
			print "Skipped a contour, not a cool contour"
		else:
			# draw rectangle around the detected object and a red point in the center of its base
			cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
			cv2.circle(frame, basePoint, 3, (0, 0, 255), 2)
			
			# get the top-view absolute coordinates
			(xb, yb) = heatmap.getPosAbsoluteCoordinates((xbRel, ybRel), (xb1, yb1))

			# draw overlayed opacity circle every 5 frames
			if frameCount % 5 == 0:
				heatmap.drawOpacityCircle(xb, yb, 255, 0, 0, 0, 15)

	# display all windows
	cv2.imshow('frame',frame)
	# UNCOMMENT IF YOU WANT TO DEBUG
	# cv2.setMouseCallback('frame', leftClickDebug)
	cv2.imshow('thresh',thresh)
	cv2.imshow('field',field)

	# wait for key press
	key = cv2.waitKey(1) & 0xFF

	# if the `q` key is pressed, break from the loop
	if key == ord("q"):
		break

# release the video source and close opened windows
video.release()
cv2.destroyAllWindows()