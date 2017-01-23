
def getAction(lastActions, minRaise, maxRaise, potSize, myBank, hand, boardCards, x, dk):
	board = [card.num for card in boardCards]
	Arating = x.evaluate([hand[0].num, hand[1].num], board)
	SwitchOneAvg = 0
	SwitchTwoAvg = 0
	given = board + [hand[0].num] + [hand[1].num]
	full = dk.GetFullDeck()
	possible = set(full)-set(given)
	for card in possible:
		switchOne = [hand[1].num, card]
		switchTwo = [hand[0].num, card]
		SwitchOneAvg += x.evaluate(switchOne, board)
		SwitchTwoAvg += x.evaluate(switchTwo, board)
			
	SwitchOneAvg = SwitchOneAvg / (len(full)-len(given))
	SwitchTwoAvg = SwitchTwoAvg / (len(full)-len(given))
	
	if Arating < SwitchOneAvg and Arating < SwitchTwoAvg:
		return "CALL\n"
	elif SwitchOneAvg < Arating and SwitchOneAvg < SwitchTwoAvg:
		return "DISCARD:"+str(hand[0])+"\n"
	else:
		return "DISCARD:"+str(hand[1])+"\n"

