previousTen = []

def getRunningAverageCoordinates(currPos, historySize = 10, maxDistance = 250):
	"""Get average position coordinates based on the last N positions.

	Args:
		currPos (tuple): Current position coordinates.
		historySize (int): Number of previous position coordinates store.
		maxDistance (int): Maximum accepted change of coordinates between successive position.

	Returns:
		tuple: Averaged coordinates (x,y).

	"""
	outsideOfMaxDistanceRange = False

	# calculate distance from previous currPos
	if len(previousTen) > 0:
		previousPoint = previousTen[0]
		distance = abs(previousPoint[0] - currPos[0]), abs(previousPoint[1] - currPos[1])
		if distance[0] > maxDistance or distance[1] > maxDistance:
			outsideOfMaxDistanceRange = True

	if outsideOfMaxDistanceRange == False:
		# insert in the coordinate history
		previousTen.insert(0, currPos)
		# remove older history records
		del previousTen[historySize:]

	# get average from all points in previousTen
	avgX = sum([currPos[0] for currPos in previousTen]) / len(previousTen)
	avgY = sum([currPos[1] for currPos in previousTen]) / len(previousTen)

	return (avgX, avgY)