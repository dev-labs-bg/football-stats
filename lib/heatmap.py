import cv2
from lib.coordinate_transform import windowToFieldCoordinates
from lib.average_coordinates import getRunningAverageCoordinates

class Heatmap:
	def __init__(self, frame, field_width, field_height):
		self.frame = frame
		self.fieldWidth = field_width
		self.fieldHeight = field_height

	# translate the basepoint's perspective coordinates to top-view ones (relative to the fields' top-left point) 
	def getPosRelativeCoordinates(self, basepoint, x1, y1, x2, y2, x3, y3, x4, y4):
		resultCoord = windowToFieldCoordinates(basepoint, x1, y1, x2, y2, x3, y3, x4, y4, self.fieldWidth, self.fieldHeight)
		x = int(resultCoord[0])
		y = int(resultCoord[1])

		return (x, y)

	# get the absolute top-view coordinates for the position
	def getPosAbsoluteCoordinates(self, pos_relative, field_top_left_point):
		(x1, y1) = field_top_left_point
		pos_relative_avg = getRunningAverageCoordinates(pos_relative)
		x = x1 + int(pos_relative_avg[0])
		y = y1 + int(pos_relative_avg[1])

		return (x, y)

	# draw overlayed opacity circle
	def drawOpacityCircle(self, x, y, color_r, color_g, color_b, radius, thickness):
		overlay = self.frame.copy()
		cv2.circle(overlay, (x, y), radius, (color_b, color_g, color_r), thickness)
		alpha = 0.25
		cv2.addWeighted(overlay, alpha, self.frame, 1 - alpha, 0, self.frame)
