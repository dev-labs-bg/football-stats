import cv2

class Mouse:
	x = 0
	y = 0
	clicked = False

	def left_click(self,event,x,y,flags,param):
		if event == cv2.EVENT_LBUTTONDOWN:
			self.x = x
			self.y = y
			self.clicked = True