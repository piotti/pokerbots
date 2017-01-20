def evalFlop(boardCards, holeCardOne, holeCardTwo):
	holes = [holeCardTwo, holeCardOne]
	flushChance = flush(boardCards, holes)
	straightChance = 0.0
	pair = pair(boardCards, holes)
	twoPair = twoPair(boardCards, holes)
	trip = triple(boardCards, holes)
	qd = quad(boardCards, holes)
	highCardVal = max([c.val for c in boardCards ], [d.val for d in holes])


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
		return 0.0

def pair(board, holes):
	boardVals = [v.val for v in board]
	holevals = [y.val for y in holes]
	return len(boardVals+holevals) != len(set(boardVals+holevals))

def twoPair(board, holes):
	boardVals = [v.val for v in board]
	holevals = [y.val for y in holes]
	return len(boardVals+holevals)-2 == len(set(boardVals+holevals))

def triple(board, holes):
	boardVals = [v.val for v in board]
	holevals = [y.val for y in holes]
	return len(boardVals+holevals)-3 == len(set(boardVals+holevals))

def quad(board, holes):
	boardVals = [v.val for v in board]
	holevals = [y.val for y in holes]
	return len(boardVals+holevals)-4 == len(set(boardVals+holevals))

		

