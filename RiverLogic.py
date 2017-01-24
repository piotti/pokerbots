import itertools
def getAction(button, lastActions, minRaise, maxRaise, potSize, myBank, hand, board, x, dk):
	boardNums = [boardCard.num for boardCard in board]
	rating = x.evaluate([hand[0].num]+[hand[1].num], boardNums)
	score = x.get_rank_class(rating)
	given = boardNums + [hand[0].num] + [hand[1].num]
	raised = lastActions[-1].typ == 'RAISE'
	raise_amount = min(max(minRaise, 0.5*potSize), maxRaise)
	ratio_bb = 0
	if score < 8:
		return "RAISE:" +str(raise_amount)+"\n"

	full = dk.GetFullDeck()
	possible = set(full)-set(given)
	might = list(itertools.combinations(list(possible), 2))
	rat = 0
	for c in might:
		tempScore = x.evaluate([c[0]]+[c[1]], boardNums)
		if tempScore > score:
			rat += 1
	rat = rat / len(might)
	if rat > .50:
		return "CHECK\n"
		
	if rat < .45:
		return "RAISE:" +str(raise_amount)+"\n"
	else:
		return "CALL\n"