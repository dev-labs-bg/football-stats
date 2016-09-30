import cv2
from lib.coordinate_transform import windowToFieldCoordinates
from lib.average_coordinates import getRunningAverageCoordinates

class Heatmap:
	def __init__(self, frame, fieldWidth, fieldHeight):
		self.frame = frame
		self.fieldWidth = fieldWidth
		self.fieldHeight = fieldHeight

	def getPosRelativeCoordinates(self, originalPoint, perspectiveCoords):
		"""Get 2D top-view coordinates (relative to the fields' top-left point) by
			translating the originalPoint's perspective coordinates.

		Args:
			originalPoint (tuple): Current position coordinates in the perspective view.
			perspectiveCoords (list): Perspective field's 4 points' coordinates.

		Returns:
			tuple: Coordinates (x,y).

		"""
		resultCoord = windowToFieldCoordinates(originalPoint, perspectiveCoords, self.fieldWidth, self.fieldHeight)
		x = int(resultCoord[0])
		y = int(resultCoord[1])

		return (x, y)

	def getPosAbsoluteCoordinates(self, posRelative, fieldTopLeftPoint):
		"""Get 2D top-view's absolute coordinates.

		Args:
			posRelative (tuple): The position's 2D top-view coordinates (relative to the fields' top-left point) .
			fieldTopLeftPoint (tuple): The 2D top-view field's top-left point coordinates.

		Returns:
			tuple: Coordinates (x,y).

		"""
		(x1, y1) = fieldTopLeftPoint
		posRelativeAvg = getRunningAverageCoordinates(posRelative)
		x = x1 + int(posRelativeAvg[0])
		y = y1 + int(posRelativeAvg[1])

		return (x, y)

	def drawOpacityCircle(self, position, colorR, colorG, colorB, radius, thickness):
		"""Draw an overlayed opacity circle.

		Args:
			position (tuple): Coordinates for the center of the circle.
			colorR (int): Red color.
			colorG (int): Green color.
			colorB (int): Blue color.
			radius (int): Radius of the circle.
			thickness (int): Thickness of the circle's line/border.

		"""
		overlay = self.frame.copy()
		cv2.circle(overlay, position, radius, (colorB, colorG, colorR), thickness)
		alpha = 0.25
		cv2.addWeighted(overlay, alpha, self.frame, 1 - alpha, 0, self.frame)
