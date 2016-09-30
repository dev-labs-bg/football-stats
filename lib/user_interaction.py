import cv2
from lib.coordinate_transform import windowToFieldCoordinates

def getPerpectiveCoordinates(image, windowName, mouse):
	"""Get coordinates of 4 points by providing them with mouse clicks.
	
	Args:
		image: Image.
		windowName (string): Name of the window showing the image.
		mouse: Mouse object.

	Returns:
		list: An array of 4 items holding coordinate tuples (x,y).

	"""
	cv2.imshow(windowName, image)	
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