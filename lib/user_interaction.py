import cv2
from lib.coordinate_transform import windowToFieldCoordinates

# get coordinates of 4 points by providing them with mouse clicks
def getPerpectiveCoordinates(frame, windowName, mouse):
	cv2.imshow(windowName, frame)	
	cv2.setMouseCallback(windowName, mouse.leftClick)
	
	i = 0
	coords = []
	
	while i < 4:
		i += 1
		mouse.x = 0
		mouse.y = 0
		mouse.leftClicked = False
		
		while mouse.leftClicked == False:
			# wait for key press
			key = cv2.waitKey(1) & 0xFF
		
		coords.append((mouse.x, mouse.y))

	return coords

# debug coordinates by moving the mouse
def leftClickDebug(event, x, y, flags, param, coords, resultWidth, resultHeight):
	if event == cv2.EVENT_LBUTTONDOWN:
		(x1, y1) = coords[0]
		(x2, y2) = coords[1]
		(x3, y3) = coords[2]
		(x4, y4) = coords[3]

		resultCoord = windowToFieldCoordinates(x, y, x1, y1, x2, y2, x3, y3, x4, y4, resultWidth, resultHeight)
	
		print "Coordinates to real coordinates", resultCoord