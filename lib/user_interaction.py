import cv2
from lib.coordinate_transform import windowToFieldCoordinates

# get coordinates of 4 points by providing them with mouse clicks
def getPerpectiveCoordinates(frame, window_name, mouse):
	cv2.imshow(window_name, frame)	
	cv2.setMouseCallback(window_name, mouse.left_click)
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

	return coords

# debug coordinates by moving the mouse
def clickDebug(event,x,y,flags,param, coords, resultWidth, resultHeight):
	(x1, y1) = coords[0]
	(x2, y2) = coords[1]
	(x3, y3) = coords[2]
	(x4, y4) = coords[3]

	resultCoord = windowToFieldCoordinates(x, y, x1, y1, x2, y2, x3, y3, x4, y4, resultWidth, resultHeight)
	
	print "Coordinates to real coordinates", resultCoord