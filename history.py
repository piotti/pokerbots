class history:
	def __init__(self):
		# (Button, not button)

		self.stats = {}
		'''
			self.preFlopRaise = ()
			self.preFlopRaiseB = (0,0)
			self.preFlopRaiseL = (0,0)
			self.threeBetB = (0,0)
			self.threeBetL = (0,0)
			self.foldToThreeBetB = (0,0)
			self.foldToThreeBetL = (0,0)
			self.fourBetB = (0,0)
			self.fourBetL = (0,0)
			self.voluntaryIntoPotB = (0,0)
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
		'''

		self.hands = {}
		self.actions = {}

		### Fields relating to current hand ###
		self.preFlopRaiseNum = 0
		self.preFlopOurRaiseNum = 0
		self.preFlopCallNum = 0


		self.postFlopRaiseNum = 0
		self.postFlopOurRaiseNum = 0
		self.postFlopBet = False
		self.postFlopUsBet = False

		self.turnRaiseNum = 0
		self.turnOurRaiseNum = 0
		self.turnBet = False
		self.turnUsBet = False

	def updateStats(self, *key):
		self.stats[key] = self.stats.get(key, 0) + 1

	def addAction(self, action, **kwargs):
		if action not in self.actions:
			self.actions[action] = []
		self.actions[action].append(kwargs)

		if action == 'RAISE':
			if kwargs['handState'] == 0:
				self.preFlopRaiseNum += 1

				#Check for 3,4,5 bets
				if self.preFlopRaiseNum == 1:
					self.updateStats('preFlopRaise', kwargs['button'])
				elif self.preFlopRaiseNum == 2 and self.preFlopOurRaiseNum == 1:
					self.updateStats('preFlopThreeBet', kwargs['button'])
				elif self.preFlopRaiseNum == 2 and self.preFlopOurRaiseNum == 2:
					self.updateStats('preFlopFourBet', kwargs['button'])
				elif self.preFlopRaiseNum == 3 and self.preFlopOurRaiseNum == 2:
					self.updateStats('preFlopFiveBet', kwargs['button'])

				#Check for voluntary into pot
				if self.preFlopCallNum == 0 and kwargs['button']:
					self.updateStats('voluntaryIntoPot')

			elif kwargs['handState'] == 2:

				#Check for continuation bet
				self.postFlopRaiseNum += 1
				if self.postFlopRaiseNum == 1 and self.preFlopRaiseNum > 0 and not self.postFlopBet:
					self.updateStats('flopContinuationBet', kwargs['button'])

				#Check for 3,4,5 bets
				if self.postFlopRaiseNum == 2 and self.postFlopOurRaiseNum == 1:
					self.updateStats('postFlopThreeBet', kwargs['button'])
				elif self.postFlopRaiseNum == 2 and self.postFlopOurRaiseNum == 2:
					self.updateStats('postFlopFourBet', kwargs['button'])
				elif self.postFlopRaiseNum == 3 and self.postFlopOurRaiseNum == 2:
					self.updateStats('postFlopFiveBet', kwargs['button'])

			elif kwargs['handState'] == 4:

				#Check for continuation bet
				self.turnRaiseNum += 1
				if self.turnRaiseNum == 1 and self.postFlopRaiseNum > 0 and not self.turnBet:
					self.updateStats('turnContinuationBet', kwargs['button'])

		elif action == 'FOLD':
			if kwargs['handState'] == 0:

				#Check for folds to 3,4,5 bets
				if self.preFlopOurRaiseNum == 1 and self.preFlopRaiseNum == 1:
					self.updateStats('preFlopFoldToThreeBet', kwargs['button'])
				elif self.preFlopOurRaiseNum == 2 and self.preFlopRaiseNum == 1:
					self.updateStats('preFlopFoldToFourBet', kwargs['button'])
				elif self.preFlopOurRaiseNum == 2 and self.preFlopRaiseNum == 2:
					self.updateStats('preFlopFoldToFiveBet', kwargs['button'])

			
			elif kwargs['handState'] == 2:

				#Check for fold to continuation
				if self.postFlopUsBet and self.postFlopRaiseNum == 0 and self.preFlopOurRaiseNum > 1:
					self.updateStats('flopFoldToContinuationBet', kwargs['button'])

				#Check for folds to 3,4,5 bets
				if self.postFlopOurRaiseNum == 1 and self.postFlopRaiseNum == 1:
					self.updateStats('postFlopFoldToThreeBet', kwargs['button'])
				elif self.postFlopOurRaiseNum == 2 and self.postFlopRaiseNum == 1:
					self.updateStats('postFlopFoldToFourBet', kwargs['button'])
				elif self.postFlopOurRaiseNum == 2 and self.postFlopRaiseNum == 2:
					self.updateStats('postFlopFoldToFiveBet', kwargs['button'])

		elif action == 'CALL':
			self.preFlopCallNum += 1

		elif action == 'BET':
			if kwargs['handState'] == 2:

				#Check for continuation bet
				if self.preFlopRaiseNum > 0 and not self.postFlopBet:
					self.updateStats('flopContinuationBet', kwargs['button'])
				self.postFlopBet = True


	def addHand(self, handId, hand):
		self.hands[handId] = hand


	def newHand(self, hand, button):
		self.preFlopRaiseNum = 0
		self.preFlopOurRaiseNum = 0
		self.preFlopCallNum = 0
		self.postFlopRaiseNum = 0


	def update(self, action, handState):
		if action == 'RAISE':
			if handState == 0:
				self.preFlopOurRaiseNum += 1
			elif handState == 2:
				self.postFlopOurRaiseNum += 1
				self.postFlopUsBet = True
		elif action == 'BET':
			if handState == 2:
				self.postFlopUsBet = True








