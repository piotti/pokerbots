def evalFlop(boardCards, holeCardOne, holeCardTwo):
	new = [holeCardTwo, holeCardOne]
	for card in boardCards:
		new.append(card)
	
	flushChance = 0.0
	straightChance = 0.0
	pair = False
	twoPair = False
	triple = False
	quad = False
	highCardVal = None

	
