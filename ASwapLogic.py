def getAction(button, lastActions, minRaise, maxRaise, potSize, myBank, hand, board, x):
	handNums = [card.num for card in hand]
	boardNums = [boardCard.num for boardCard in board]
	rating = x.evaluate(handNums, boardNums)
	score = x.get_rank_class(rating)
	scoreReal = x.class_to_string(score)
	if scoreReal != "High Card" or scoreReal != 'Pair':
		print scoreReal, "good hand"
	
	action = "CALL\n"
	return action