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

"""
Simple example pokerbot, written in python.

This is an example of a bare bones pokerbot. It only sets up the socket
necessary to connect with the engine and then always returns the same action.
It is meant as an example of how a pokerbot should communicate with the engine.
"""

FACE_VALS = ['2','3','4','5','6','7','8','9','T','J','Q','K','A']
SUIT_BIN = ['s','h','d','c']
PAIR_ODDS = [49.39, 52.84, 56.26, 59.64, 62.7, 65.73, 68.72, 71.67, 74.66, 77.15, 79.63, 82.12, 84.9]
x = Evaluator()

'''
HANDSTATES:
0 - After Post, preflop
1 - After flop, discarding
2 - After discard, betting
3 - After turn, discarding
4 - After discard, betting
5 - After river
'''
class Action:
    def __init__(self, s):
        self.s = s
        parts = s.split(':')
        self.typ = parts[0]
        if len(parts) > 1:
            self.v1 = parts[1]
            if len(parts) > 2:
                self.v2 = parts[2]
            if len(parts) > 3:
                self.v3 = parts[3]
    def __str__(self):
        return self.s
    def __repr__(self):
        return self.s

class Card:
    def __init__(self, s):
        self.s = s
        self.num = DeucesCard.new(s)
        self.fv = s[0]
        self.suit = s[1]
    def __str__(self):
        return self.s


class Player:
    def run(self, input_socket):
        # Get a file-object for reading packets from the socket.
        # Using this ensures that you get exactly one packet per read.
        f_in = input_socket.makefile()
        hole_odds_dict = pickle.load(open('odds.pkl', 'rb'))
        for i in range(13):
            hole_odds_dict[(FACE_VALS[i]+'/'+FACE_VALS[i], False)] = PAIR_ODDS[i]

        record = h.history()
        while True:
            # Block until the engine sends us a packet.
            data = f_in.readline().strip()
            # If data is None, connection has closed.
            if not data:
                print "Gameover, engine disconnected."
                break

            # Here is where you should implement code to parse the packets from
            # the engine and act on it. We are just printing it instead.

            
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


            elif word == "GETACTION":


                [potSize, numBoardCards] = [int(e) for e in parts[1:3]]
                boardCards = [Card(e) for e in parts[3:3+numBoardCards]]
                numLastActions = int(parts[3+numBoardCards])
                lastActions = [Action(e) for e in parts[4+numBoardCards:4+numBoardCards+numLastActions]]
                numLegalActions = int(parts[4+numBoardCards+numLastActions])
                legalActions = [Action(e) for e in parts[5+numBoardCards+numLastActions:5+numBoardCards+numLastActions+numLegalActions]]

                last_action = lastActions[-1]

                print lastActions

                recordInfo = {'handId':handId, 'handState':HAND_STATE, 'button':button, 'boardCards':boardCards}
                addRecord = False

                for a in lastActions[1:]:
                    if a.typ == 'POST':
                        HAND_STATE = 0
                        call_amount = bb//2 if button else 0
                    elif a.typ == 'DEAL':
                        if a.v1 == 'FLOP':
                            HAND_STATE = 1
                        elif a.v1 == 'TURN':
                            HAND_STATE = 3
                        elif a.v1 == 'RIVER':
                            HAND_STATE = 5
                        call_amount = 0
                    elif a.typ == 'BET':
                        call_amount += int(a.v1)
                        #update history that player bet x
                        addRecord = True
                    elif a.typ == 'CALL':
                        addRecord = True
                        recordInfo['callAmount'] = callAmount
                        call_amount = 0
                    elif a.typ == 'CHECK':
                        addRecord = True
                        call_amount = 0
                        if HAND_STATE in (1, 3) and not button:
                            HAND_STATE += 1
                    elif a.typ == 'FOLD':
                        addRecord = True
                        recordInfo['callAmount'] = callAmount
                        HAND_STATE += 1
                        call_amount = 0
                    elif a.typ == 'DISCARD':
                        addRecord = True
                        if not button:
                            HAND_STATE += 1
                    elif a.typ == 'RAISE':
                        call_amount += int(a.v1)
                    elif a.typ == 'SHOW':
                        record.addHand(handId, Card(a.v1), Card(a.v2))
                    elif a.typ == 'TIE':
                        #keep track of this stat
                        pass
                    elif a.typ == 'WIN':
                        #keep track of this stat
                        pass

                    if addRecord:
                        record.addAction(a.typ, **recordInfo)


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
                        minRaise = int(e.v1)
                        maxRaise = int(e.v2)
                        break

                if preflop:
                    record.updatePreflopStats(button, last_action)
                    action = prefL.getAction(lastActions, minRaise, maxRaise, bb, potSize, myBank, hand, hole_odds)
                    s.send(action)
                
                #goes to flop before swap logic
                elif BswapLogicFlop:
                    record.updateFlopStats()
                    action = BSLF.getAction()
                    s.send(action)

                #goes to flop after swap logic
                elif AswapLogicFlop:
                    record.updateFlopStats()
                    action = ASLF.getAction(button, lastActions, minRaise, maxRaise, potSize, myBank, hand, boardCards, x)
                    s.send(action)

                #goes to 4th card before swap logic
                elif BswapLogicTurn:
                    record.updateTurnStats()
                    action = BSLR.getAction()
                    s.send(action)

                #goes to 4th card after swap logic
                elif AswapLogicTurn:
                    record.updateTurnStats()
                    action = ASLR.getAction()
                    s.send(action)

                #goes to showdown logic
                else:
                    record.updateShowdownStats()
                    action = RL.getAction()
                    s.send(action) 

                
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
    args = parser.parse_args()

    # Create a socket connection to the engine.
    print 'Connecting to %s:%d' % (args.host, args.port)
    try:
        s = socket.create_connection((args.host, args.port))
    except socket.error as e:
        print 'Error connecting! Aborting'
        exit()

    bot = Player()
    bot.run(s)
