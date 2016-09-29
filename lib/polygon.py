import cv2

# draw a quadrilateral in a given window by providind 4 points' coordinates, line color and thickness
def drawQuadrilateral(frame, x1, y1, x2, y2, x3, y3, x4, y4, colorR, colorG, colorB, lineThickness):
	cv2.line(frame, (x1, y1), (x2, y2), (colorB, colorG, colorR), lineThickness)
	cv2.line(frame, (x2, y2), (x3, y3), (colorB, colorG, colorR), lineThickness)
	cv2.line(frame, (x3, y3), (x4, y4), (colorB, colorG, colorR), lineThickness)
	cv2.line(frame, (x4, y4), (x1, y1), (colorB, colorG, colorR), lineThickness)