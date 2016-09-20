previousTen = []
def getRunningAverageCoordinates(basepoint, historySize = 10, maxDistance = 250):
	outsideOfMaxDistanceRange = False

	# calculate distance from previous basepoint
	if len(previousTen) > 0:
		previousPoint = previousTen[0]
		distance = abs(previousPoint[0] - basepoint[0]), abs(previousPoint[1] - basepoint[1])
		if distance[0] > maxDistance or distance[1] > maxDistance:
			outsideOfMaxDistanceRange = True

	if outsideOfMaxDistanceRange == False:
		# insert in the coordinate history
		previousTen.insert(0, basepoint)
		# remove older history records
		del previousTen[historySize:]

	# get average from all points in previousTen
	avgX = sum([basepoint[0] for basepoint in previousTen]) / len(previousTen)
	avgY = sum([basepoint[1] for basepoint in previousTen]) / len(previousTen)

	return (avgX, avgY)