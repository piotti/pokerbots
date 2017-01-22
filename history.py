class history:
	def __init__(self):
		self.preFlopUpdates = 0
		self.preFlopRaiseB = 0
		self.preFlopRaiseL = 0
		self.threeBetB = 0.0
		self.threeBetL = 0.0
		self.foldToThreeBetB = 0.0
		self.foldToThreeBetL = 0.0
		self.fourBetB = 0.0
		self.fourBetL = 0.0
		self.voluntaryIntoPotB = 0.0
		self.voluntaryIntoPotL = 0.0

		self.flopUpdates = 0
		self.flopContinuationBet = 0.0
		self.flopFoldToContinuationBet = 0.0
		self.flopCheckRaise = 0.0
		self.flopThreeBet = 0.0
		self.flopFoldToThreeBet = 0.0
		self.flopFourBet = 0.0
		self.flopFoldToFourBet = 0.0

		self.TurnUpdates = 0
		self.TurnContinuationBet = 0.0
		self.TurnFoldToContinuationBet = 0.0
		self.TurnCheckRaise = 0.0
		self.TurnThreeBet = 0.0
		self.TurnFoldToThreeBet = 0.0
		self.TurnFourBet = 0.0
		self.TurnFoldToFourBet = 0.0

		self.showdownUpdates = 0
		self.showdownContinuationBet = 0.0
		self.showdownFoldToContinuationBet = 0.0
		self.showdownCheckRaise = 0.0
		self.showdownThreeBet = 0.0
		self.showdownFoldToThreeBet = 0.0
		self.showdownFourBet = 0.0
		self.showdownFoldToFourBet = 0.0

		self.hands = {}
		self.actions = {}

		### Fields relating to current hand ###
		self.log = []

	def addAction(self, action, **kwargs):
		if action not in self.actions:
			self.actions[action] = []
		self.actions[action].append(kwargs)
	def addHand(self, handId, hand):
		self.hands[handId] = hand


	def newHand(self, hand, button):
		self.log = []

	def update(self, action, us=False):
		pass
		

	def updateMultiple(self, actions):
		for a in actions:
			self.update(a)



	def updatePreflopStats(self, button, last_action):
		pass
		self.preFlopUpdates += 1
		# if not button:
		# 	for action in lastActions:

		# else:



	def updateFlopStats(self):
		pass

	def updateTurnStats(self):
		pass

	def updateShowdownStats(self):
		pass








