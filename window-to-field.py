import argparse
import cv2
import time
import numpy as np

# this is the badass algorithm, from openCV, as mine didn't work :(
def windowToFieldCoordinatesX(xp, yp, x1, y1, x2, y2, x3, y3, x4, y4):
    src = np.array([
        [x1, y1],
        [x2, y2],
        [x3, y3],
        [x4, y4]], dtype = "float32")

    # those should be the same aspect as the real width/height of field
    maxWidth = x4-x1
    maxHeight = y1-y2

    # make a destination rectangle with the width and height of above (starts at 0,0)
    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype = "float32")

    # find the transformation matrix for our transforms
    transformationMatrix = cv2.getPerspectiveTransform(src, dst)

    # put the original (source) x,y points in an array (not sure why do we have to put it 3 times though)    
    original = np.array([((xp, yp), (xp, yp), (xp, yp))], dtype=np.float32)

    # use perspectiveTransform to transform our original(mouse coords) to new coords with the transformation matrix
    transformed = cv2.perspectiveTransform(original, transformationMatrix)[0][0]

    return transformed


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
	camera = cv2.VideoCapture(os.path.join( args["video"] ))

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
        valueFromAlgorithm = windowToFieldCoordinatesX(coordX, coordY, bottomLeft[0], bottomLeft[1], topLeft[0], topLeft[1], topRight[0], topRight[1], bottomRight[0], bottomRight[1])
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
