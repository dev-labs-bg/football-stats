import cv2

# apply color subtractions and calculations to get a black and white frame
#
# arguments:
# fgbg		BackgroundSubtractorMOG2 object
# frame
def getThresholdedFrame(fgbg, frame):
	# apply background subtraction on the frame
	fgmask = fgbg.apply(frame, learningRate=0.02)
	
	# blur the frame
	fgmask = cv2.GaussianBlur(fgmask, (21, 21), 0)
	
	# apply threshold, turning the frame into pure black and white
	thresh = cv2.threshold(fgmask, 25, 255, cv2.THRESH_BINARY)[1]
	
	# dilate the frame, making the white objects' borders smoother and easier for contour extraction
	thresh = cv2.dilate(thresh, None, iterations=3)

	return thresh