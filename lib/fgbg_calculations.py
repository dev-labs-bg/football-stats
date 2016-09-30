import cv2

def getThresholdedFrame(fgbg, image):
	"""Apply color subtractions and calculations to get a purely black and white image.

	Args:
		fgbg: cv::BackgroundSubtractorMOG2 object.
		image: Image.

	Returns:
		Image.
	
	"""
	# apply background subtraction on the image
	fgmask = fgbg.apply(image, learningRate=0.02)
	
	# blur the image
	fgmask = cv2.GaussianBlur(fgmask, (21, 21), 0)
	
	# apply threshold, turning the image into pure black and white
	thresh = cv2.threshold(fgmask, 25, 255, cv2.THRESH_BINARY)[1]
	
	# dilate the image, making the white objects' borders smoother and easier for contour extraction
	thresh = cv2.dilate(thresh, None, iterations=3)

	return thresh