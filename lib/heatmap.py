import cv2
from lib.coordinate_transform import windowToFieldCoordinates
from lib.average_coordinates import getRunningAverageCoordinates

class Heatmap:
	def __init__(self, frame, fieldWidth, fieldHeight):
		self.frame = frame
		self.fieldWidth = fieldWidth
		self.fieldHeight = fieldHeight

	# translate the basepoint's perspective coordinates to top-view ones (relative to the fields' top-left point) 
	def getPosRelativeCoordinates(self, basePoint, x1, y1, x2, y2, x3, y3, x4, y4):
		resultCoord = windowToFieldCoordinates(basePoint, x1, y1, x2, y2, x3, y3, x4, y4, self.fieldWidth, self.fieldHeight)
		x = int(resultCoord[0])
		y = int(resultCoord[1])

		return (x, y)

	# get the absolute top-view coordinates for the position
	def getPosAbsoluteCoordinates(self, posRelative, fieldTopLeftPoint):
		(x1, y1) = fieldTopLeftPoint
		posRelativeAvg = getRunningAverageCoordinates(posRelative)
		x = x1 + int(posRelativeAvg[0])
		y = y1 + int(posRelativeAvg[1])

		return (x, y)

	# draw overlayed opacity circle
	def drawOpacityCircle(self, x, y, colorR, colorG, colorB, radius, thickness):
		overlay = self.frame.copy()
		cv2.circle(overlay, (x, y), radius, (colorB, colorG, colorR), thickness)
		alpha = 0.25
		cv2.addWeighted(overlay, alpha, self.frame, 1 - alpha, 0, self.frame)
