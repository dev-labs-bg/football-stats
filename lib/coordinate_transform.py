import argparse
import cv2
import time
import numpy as np

# this is the badass algorithm, from openCV, as mine didn't work :(
def windowToFieldCoordinates(basepoint, x1, y1, x2, y2, x3, y3, x4, y4, maxWidth=0, maxHeight=0):
    (xp, yp) = basepoint
    src = np.array([
        [x1, y1],
        [x2, y2],
        [x3, y3],
        [x4, y4]], dtype = "float32")

    # those should be the same aspect as the real width/height of field
    maxWidth = (x4-x1) if maxWidth == 0 else maxWidth
    maxHeight = (y1-y2) if maxHeight == 0 else maxHeight

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