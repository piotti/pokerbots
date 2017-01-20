def evalFlop(boardCards, holeCardOne, holeCardTwo):
	new = [holeCardTwo, holeCardOne]
	flushChance = flush(board,holes)
	straightChance = 0.0
	pair = False
	twoPair = False
	triple = False
	quad = False
	highCardVal = None


def flush(board, holes):
	numberOfCards = len(full+holes)
	holeSuits = [hole.suitVal for hole in holes]
	holeSuitsLen = len(set(holeSuits)) 
	boardSuits = [b.suitVal for b in board]
	boardSuitsLen = len(set(boardSuits))
	fullSuitsLen = len(set(boardSuits + holeSuits))
	if fullSuitsLen == 1:
		return 1.0 

		#need to get this right
	elif numberOfCards == 5:
		if fullSuitsLen == 2 and holeSuitsLen == 1:
			return .16
		else:
			return 0.0

	elif numberOfCards == 6:
		if fullSuitsLen == 2 and holeSuitsLen == 1:
			return .08
		else:
			return 0.0
	else:
		return 0


		

