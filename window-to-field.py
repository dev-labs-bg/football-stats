import argparse
import cv2
import time
import numpy as np
from coordinate_transform import windowToFieldCoordinates

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
ap.add_argument("-a", "--min-area", type=int, default=300, help="minimum area size")
args = vars(ap.parse_args())
# if the video argument is None, then we are reading from webcam
if args.get("video", None) is None:
	camera = cv2.VideoCapture(0)
	time.sleep(0.25)
# otherwise, we are reading from a video file
else:
	camera = cv2.VideoCapture(args["video"])

while True:
    ret, img = camera.read()

    bottomLeft = [100, 400, 0]
    topLeft = [220, 200, 0]
    topRight = [270, 200, 0]
    bottomRight = [400, 400, 0]

    fieldOnCameraColor = (0, 255, 0)
    fieldProjectedColor = (0, 125, 125)

    # draw field
    cv2.line(img, (int(bottomLeft[0]), int(bottomLeft[1])), (int(topLeft[0]), int(topLeft[1])), fieldOnCameraColor, 2)
    cv2.line(img, (int(topLeft[0]), int(topLeft[1])), (int(topRight[0]), int(topRight[1])), fieldOnCameraColor, 2)
    cv2.line(img, (int(topRight[0]), int(topRight[1])), (int(bottomRight[0]), int(bottomRight[1])), fieldOnCameraColor, 2)
    cv2.line(img, (int(bottomRight[0]), int(bottomRight[1])), (int(bottomLeft[0]), int(bottomLeft[1])), fieldOnCameraColor, 2)

    def toFieldCoord(coordX, coordY):
        # call the algorithm
        valueFromAlgorithm = windowToFieldCoordinates(coordX, coordY, bottomLeft[0], bottomLeft[1], topLeft[0], topLeft[1], topRight[0], topRight[1], bottomRight[0], bottomRight[1])
        return valueFromAlgorithm
    
    bottomLeftField = toFieldCoord(bottomLeft[0], bottomLeft[1])
    bottomRightField = toFieldCoord(bottomRight[0], bottomRight[1])
    topLeftField = toFieldCoord(topLeft[0], topLeft[1])
    topRightField = toFieldCoord(topRight[0], topRight[1])

    # draw field
    cv2.line(img, (int(bottomLeftField[0]), int(bottomLeftField[1])), (int(topLeftField[0]), int(topLeftField[1])), fieldProjectedColor, 2)
    cv2.line(img, (int(topLeftField[0]), int(topLeftField[1])), (int(topRightField[0]), int(topRightField[1])), fieldProjectedColor, 2)
    cv2.line(img, (int(topRightField[0]), int(topRightField[1])), (int(bottomRightField[0]), int(bottomRightField[1])), fieldProjectedColor, 2)
    cv2.line(img, (int(bottomRightField[0]), int(bottomRightField[1])), (int(bottomLeftField[0]), int(bottomLeftField[1])), fieldProjectedColor, 2)

    # MOUSE STUFFZ
    def onmouse(event, x, y, flags, param):
        valueFromAlgorithm = toFieldCoord(x,y)
        cv2.circle(img, (valueFromAlgorithm[0], valueFromAlgorithm[1]), 10, (255, 0, 0), 2)

        cv2.imshow('plane', img)

    cv2.imshow('plane', img)
    cv2.setMouseCallback('plane', onmouse)

    if 0xFF & cv2.waitKey(5) == 27:
        break
