import argparse
import cv2
import time
import numpy as np

def windowToFieldCoordinates(originalPoint, perspectiveCoords, width=0, height=0):
    """Get 2D coordinates by transforming inputed perspective ones.

    Args:
        originalPoint (tuple): Position coordinates of a point in the perspective view.
        perspectiveCoords (list): Perspective field's 4 points' coordinates.
        width (int): Width in pixels for the 2D top-view field.
        height (int): Height in pixels for the 2D top-view field.

    Returns:
        list: Transformed coordinates [x,y].

    """
    (xp, yp) = originalPoint
    (x1, y1) = perspectiveCoords[0]
    (x2, y2) = perspectiveCoords[1]
    (x3, y3) = perspectiveCoords[2]
    (x4, y4) = perspectiveCoords[3]

    src = np.array([
        [x1, y1],
        [x2, y2],
        [x3, y3],
        [x4, y4]], dtype = "float32")

    # those should be the same aspect as the real width/height of field
    width = (x4-x1) if width == 0 else width
    height = (y1-y2) if height == 0 else height

    # make a destination rectangle with the width and height of above (starts at 0,0)
    dst = np.array([
        [0, 0],
        [width - 1, 0],
        [width - 1, height - 1],
        [0, height - 1]], dtype = "float32")

    # find the transformation matrix for our transforms
    transformationMatrix = cv2.getPerspectiveTransform(src, dst)

    # put the original (source) x,y points in an array
    original = np.array([((xp, yp), (xp, yp), (xp, yp))], dtype=np.float32)

    # use perspectiveTransform to transform our original to new coords with the transformation matrix
    transformedCoord = cv2.perspectiveTransform(original, transformationMatrix)[0][0]

    return transformedCoord