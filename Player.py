import argparse
import socket
import sys
import pickle
import preflopLogic as prefL
import BSwapLogic as BSLF
import ASwapLogic as ASLF
import BSwapLogicRiver as BSLR
import ASwapLogicRiver as ASLR
import RiverLogic as RL
import history as h
from deuces import Card as DeucesCard
from deuces import Evaluator
from deuces import Deck

import json

"""
Dictionary containing all the parameters that could be varied in logic to optimize extracting value from hands
"""
TUNE_MODE = True



FACE_VALS = ['2','3','4','5','6','7','8','9','T','J','Q','K','A']
SUIT_BIN = ['s','h','d','c']
PAIR_ODDS = [49.39, 52.84, 56.26, 59.64, 62.7, 65.73, 68.72, 71.67, 74.66, 77.15, 79.63, 82.12, 84.9]
x = Evaluator()
dk = Deck()

'''
HANDSTATES:
0 - After Post, preflop
1 - After flop, discarding
2 - After discard, betting
3 - After turn, discarding
4 - After discard, betting
5 - After river
'''

class Card:
    def __init__(self, s):
        self.s = s
        self.num = DeucesCard.new(s)
        self.fv = s[0]
        self.suit = s[1]
    def __str__(self):
        return self.s

class Action:
    PERFORMED_ACTION_DICT = {
        'BET':[('amount', int), ('actor', str)],
        'CALL':[('actor', str)],
        'CHECK':[('actor', str)],
        'DEAL':[('street', str)],
        'FOLD':[('actor', str)],
        'POST':[('amount', int), ('actor', str)],
        'DISCARD':[('actor', str)],
        'RAISE':[('amount', int), ('actor', str)],
        'REFUND':[('amount', int), ('actor', str)],
        'SHOW':[('card1', Card), ('card2', Card), ('actor', str)],
        'TIE': [('amount', int),('actor', str)],
        'WIN': [('amount', int),('actor', str)]
    }
    LEGAL_ACTION_DICT = {
        'BET':[('minBet', int), ('maxBet', int)],
        'CALL':[],
        'CHECK':[],
        'FOLD':[],
        'DISCARD':[('actor', str)], #Card info here?
        'RAISE':[('minRaise', int), ('maxRaise', int)]
    }
    def __init__(self, s, action_type):
        self.s = s
        parts = s.split(':')
        self.typ = parts.pop(0)
        if self.typ == 'DISCARD' and action_type == 'PERFORMED' and len(parts) == 3:
            self.actor = parts[2]
            self.old = Card(parts[0])
            self.new = Card(parts[1])
            return 
        dic = Action.LEGAL_ACTION_DICT if action_type == 'LEGAL' else Action.PERFORMED_ACTION_DICT
        for i, e in enumerate(parts):
            setattr(
                self,
                dic[self.typ][i][0],
                dic[self.typ][i][1](e)
            )
    def __str__(self):
        return self.s
    def __repr__(self):
        return self.s


class Player:
    def run(self, input_socket, param_num=0):
        # Get a file-object for reading packets from the socket.
        # Using this ensures that you get exactly one packet per read.
        f_in = input_socket.makefile()
        hole_odds_dict = pickle.load(open('odds.pkl', 'rb'))
        for i in range(13):
            hole_odds_dict[(FACE_VALS[i]+'/'+FACE_VALS[i], False)] = PAIR_ODDS[i]

        record = h.history()

        global ps
        ps = json.loads(open('params.txt', 'r').read())[param_num]

        while True:
            # Block until the engine sends us a packet.
            data = f_in.readline().strip()
            # If data is None, connection has closed.
            if not data:
                print "Gameover, engine disconnected."
                break

            # Here is where you should implement code to parse the packets from
            # the engine and act on it. We are just printing it instead.

            if not TUNE_MODE:
                print data
            parts = data.split()
            word = parts[0]
            if word == "NEWGAME":
                [yourName, opp1Name, stackSize, bb, numHands, timeBank] = parts[1:]
                stackSize = int(stackSize)
                bb = int(bb)
                numHands = int(numHands)
                timeBank = float(timeBank)
            elif word == "NEWHAND":
                HAND_STATE = 0
                opp_bid_hist = []
                opp_flop_disc = False
                opp_turn_disc = False
                callAmount = 0



                [handId, button, holeCard1, holeCard2, myBank, otherBank, timeBank] = parts[1:]
                handId = int(handId)
                button = button == 'true'
                myBank = int(myBank)
                otherBank = int(otherBank)
                suited = holeCard1[1] == holeCard2[1]
                if FACE_VALS.index(holeCard1[0]) < FACE_VALS.index(holeCard2[0]):
                    hole_odds = hole_odds_dict[(holeCard1[0] + '/' + holeCard2[0], suited)]
                else:
                    hole_odds = hole_odds_dict[(holeCard2[0] + '/' + holeCard1[0], suited)]
                holeCard1 = Card(holeCard1)
                holeCard2 = Card(holeCard2)
                hand = [holeCard1, holeCard2]

                record.newHand(hand, button)


            elif word == "GETACTION":


                [potSize, numBoardCards] = [int(e) for e in parts[1:3]]
                boardCards = [Card(e) for e in parts[3:3+numBoardCards]]
                numLastActions = int(parts[3+numBoardCards])
                lastActions = [Action(e, 'PERFORMED') for e in parts[4+numBoardCards:4+numBoardCards+numLastActions]]
                numLegalActions = int(parts[4+numBoardCards+numLastActions])
                legalActions = [Action(e, 'LEGAL') for e in parts[5+numBoardCards+numLastActions:5+numBoardCards+numLastActions+numLegalActions]]

                last_action = lastActions[-1]
                if not TUNE_MODE:
                    print lastActions

                recordInfo = {'handId':handId, 'handState':HAND_STATE, 'button':button, 'boardCards':boardCards}
                addRecord = False

                for a in lastActions[1:]:
                    if a.typ == 'POST':
                        HAND_STATE = 0
                        call_amount = bb//2 if button else 0
                    elif a.typ == 'DEAL':
                        if a.street == 'FLOP':
                            HAND_STATE = 1
                        elif a.street == 'TURN':
                            HAND_STATE = 3
                        elif a.street == 'RIVER':
                            HAND_STATE = 5
                        call_amount = 0
                    elif a.typ == 'BET':
                        call_amount += a.amount
                        addRecord = True
                    elif a.typ == 'CALL':
                        addRecord = True
                        recordInfo['callAmount'] = callAmount
                        call_amount = 0
                    elif a.typ == 'CHECK':
                        addRecord = True
                        call_amount = 0
                        if HAND_STATE in (1, 3) and button:
                            HAND_STATE += 1
                    elif a.typ == 'FOLD':
                        addRecord = True
                        recordInfo['callAmount'] = call_amount
                        HAND_STATE += 1
                        call_amount = 0
                    elif a.typ == 'DISCARD':
                        addRecord = True
                        if not button:
                            HAND_STATE += 1
                    elif a.typ == 'RAISE':
                        addRecord = True
                        recordInfo['amount'] = a.amount
                        call_amount += a.amount
                    elif a.typ == 'SHOW':
                        record.addHand(handId, Card(a.card1), Card(a.card2))
                    elif a.typ == 'TIE':
                        #keep track of this stat
                        pass
                    elif a.typ == 'WIN':
                        #keep track of this stat
                        pass

                    #record.addAction(a.typ, **recordInfo)


                can_discard = False
                for e in legalActions:
                    if e.typ == 'DISCARD':
                        can_discard = True
                        break
                #indentifies preflop state
                preflop = HAND_STATE == 0
                #identifies flop before swap state
                BswapLogicFlop = HAND_STATE == 1
                #identifies flop after swap state
                AswapLogicFlop = HAND_STATE == 2
                #identifies first river card state before swap
                BswapLogicTurn = HAND_STATE == 3
                #identifies first river card state after swap
                AswapLogicTurn = HAND_STATE == 4
                #identifies showdown state
                showdown = numBoardCards == 5

                # goes to preflop logic file to get the new action
                for e in legalActions:
                    if e.typ == 'RAISE':
                        minRaise = e.minRaise
                        maxRaise = e.maxRaise
                        break

                if preflop:
                    action = prefL.getAction(lastActions,minRaise,maxRaise,bb,potSize,myBank,hand,hole_odds,ps['p_all_in_t'],ps['p_raise_t'],ps['p_call_t_one'],ps['p_call_t_two'],ps['p_bluff'])
                    s.send(action)
                
                #goes to flop before swap logic
                elif BswapLogicFlop:
                    action = BSLF.getAction(lastActions, minRaise, maxRaise, potSize, myBank, hand, boardCards, x, dk)
                    s.send(action)

                #goes to flop after swap logic
                elif AswapLogicFlop:
                    action = ASLF.getAction(button,lastActions,minRaise,maxRaise,potSize,myBank,hand,boardCards,x,dk,ps['f_check'],ps['f_raise'],ps['f_bluff'])
                    s.send(action)

                #goes to 4th card before swap logic
                elif BswapLogicTurn:
                    action = BSLR.getAction(lastActions, minRaise, maxRaise, potSize, myBank, hand, boardCards, x, dk)
                    s.send(action)

                #goes to 4th card after swap logic
                elif AswapLogicTurn:
                    action = ASLR.getAction(button,lastActions,minRaise,maxRaise,potSize,myBank,hand,boardCards,x,dk,ps['r_check'],ps['r_raise'],ps['r_bluff'])
                    s.send(action)

                #goes to showdown logic
                else:
                    action = RL.getAction(button,lastActions,minRaise,maxRaise,potSize,myBank,hand,boardCards,x,dk,ps['s_check'],ps['s_raise'],ps['s_bluff'])
                    s.send(action) 

                #record.update(action)

                
            elif word == "REQUESTKEYVALUES":
                # At the end, the engine will allow your bot save key/value pairs.
                # Send FINISH to indicate you're done.
                s.send("FINISH\n")
        # Clean up the socket.
        s.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='A Pokerbot.', add_help=False, prog='pokerbot')
    parser.add_argument('-h', dest='host', type=str, default='localhost', help='Host to connect to, defaults to localhost')
    parser.add_argument('port', metavar='PORT', type=int, help='Port on host to connect to')
    if TUNE_MODE:
        parser.add_argument('param_num', metavar='PARAM_NUM', type=int, help='Bitch you guessed it')
    args = parser.parse_args()

    # Create a socket connection to the engine.
    if not TUNE_MODE:
        print 'Connecting to %s:%d' % (args.host, args.port)
    try:
        s = socket.create_connection((args.host, args.port))
    except socket.error as e:
        print 'Error connecting! Aborting'
        exit()
    param_num = args.param_num if TUNE_MODE else 0
    bot = Player()
    bot.run(s, param_num)
