previousTen = []
def getRunningAverageCoordinates(basepoint):

	previousTen.insert(0, basepoint)

	# remove if more than 10 items
	del previousTen[10:]

	# get average from all points in previousTen
	avgX = sum([basepoint[0] for basepoint in previousTen]) / len(previousTen)
	avgY = sum([basepoint[1] for basepoint in previousTen]) / len(previousTen)

	return (avgX, avgY)