import cv2

# draw a quadrilateral in a given window by providind 4 points' coordinates, line color and thickness
def drawQuadrilateral(window, x1, y1, x2, y2, x3, y3, x4, y4, color_r, color_g, color_b, line_thickness):
	cv2.line(window, (x1, y1), (x2, y2), (color_b, color_g, color_r), line_thickness)
	cv2.line(window, (x2, y2), (x3, y3), (color_b, color_g, color_r), line_thickness)
	cv2.line(window, (x3, y3), (x4, y4), (color_b, color_g, color_r), line_thickness)
	cv2.line(window, (x4, y4), (x1, y1), (color_b, color_g, color_r), line_thickness)