class history:
	def __init__(self):
		self.preFlopUpdates = 1
		self.preFlopRaiseB = 1.0
		self.preFlopRaiseL = 1.0
		self.threeBetB = 1.0
		self.threeBetL = 1.0
		self.foldToThreeBetB = 1.0
		self.foldToThreeBetL = 1.0
		self.fourBetB = 1.0
		self.fourBetL = 1.0
		self.voluntaryIntoPotB = 1.0
		self.voluntaryIntoPotL = 1.0

		self.flopUpdates = 1.0
		self.flopContinuationBet = 1.0
		self.flopFoldToContinuationBet = 1.0
		self.flopCheckRaise = 1.0
		self.flopThreeBet = 1.0
		self.flopFoldToThreeBet = 1.0
		self.flopFourBet = 1.0
		self.flopFoldToFourBet = 1.0

		self.TurnUpdates = 1
		self.TurnContinuationBet = 1.0
		self.TurnFoldToContinuationBet = 1.0
		self.TurnCheckRaise = 1.0
		self.TurnThreeBet = 1.0
		self.TurnFoldToThreeBet = 1.0
		self.TurnFourBet = 1.0
		self.TurnFoldToFourBet = 1.0

		self.showdownUpdates = 1
		self.showdownContinuationBet = 1.0
		self.showdownFoldToContinuationBet = 1.0
		self.showdownCheckRaise = 1.0
		self.showdownThreeBet = 1.0
		self.showdownFoldToThreeBet = 1.0
		self.showdownFourBet = 1.0
		self.showdownFoldToFourBet = 1.0

	def updatePreflopStats(button, lastActions):
		self.preFlopUpdates += 1
		if not button:
			for action in lastActions:
				
		else:



	def updateFlopStats():
		pass

	def updateTurnStats():
		pass

	def updateShowdownStats():
		pass








