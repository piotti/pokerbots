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


"""
Simple example pokerbot, written in python.

This is an example of a bare bones pokerbot. It only sets up the socket
necessary to connect with the engine and then always returns the same action.
It is meant as an example of how a pokerbot should communicate with the engine.
"""

FACE_VALS = ['2','3','4','5','6','7','8','9','T','J','Q','K','A']
PAIR_ODDS = [49.39, 52.84, 56.26, 59.64, 62.7, 65.73, 68.72, 71.67, 74.66, 77.15, 79.63, 82.12, 84.9]

'''
0 - After Post, preflop
1 - After flop, pre-discard betting
2 - After discard, betting
3 - After turn, pre-discard betting
4 - After discard, betting
5 - After river
'''
class Action:
    def __init__(self, s):
        parts = s.split(':')
        self.typ = parts[0]
        if len(parts) > 1:
            self.v1 = parts[1]
            if len(parts) > 2:
                self.v2 = parts[2]
            if len(parts) > 3:
                self.v3 = parts[3]
class Card:
    def __init__(self, s):
        self.val = s[0]
        self.suit = s[1]

    def __cmp__(self, other):
        return cmp(FACE_VALS.index(self.val), FACE_VALS.index(other.val))


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
                [handId, button, holeCard1, holeCard2, myBank, otherBank, timeBank] = parts[1:]
                handId = int(handId)
                button = bool(button)
                myBank = int(myBank)
                otherBank = int(otherBank)
                holeCard1 = Card(holeCard1)
                holeCard2 = Card(holeCard2)


                suited = holeCard1.suit == holeCard2.suit
                card_key = min(holeCard1, holeCard2).val+'/'+max(holeCard1, holeCard2).val
                hole_odds = hole_odds_dict[(card_key, suited)]
                good_hand = hole_odds > 50


                print hole_odds


            elif word == "GETACTION":

                [potSize, numBoardCards] = [int(e) for e in parts[1:3]]
                boardCards = [Card(e) for e in parts[3:3+numBoardCards]]
                numLastActions = int(parts[3+numBoardCards])
                lastActions = [Action(e) for e in parts[4+numBoardCards:4+numBoardCards+numLastActions]]
                numLegalActions = int(parts[4+numBoardCards+numLastActions])
                legalActions = [Action(e) for e in parts[5+numBoardCards+numLastActions:5+numBoardCards+numLastActions+numLegalActions]]

                last_action = lastActions[-1]


                can_discard = False
                for e in legalActions:
                    if e.typ == 'DISCARD':
                        can_discard = True
                        break
                #indentifies preflop state
                preflop = numBoardCards == 0
                #identifies flop before swap state
                BswapLogicFlop = last_action.typ == 'DEAL' and last_action.v1 == 'FLOP'
                #identifies flop after swap state
                AswapLogicFlop = numBoardCards == 3 and not can_discard
                #identifies first river card state before swap
                BswapLogicTurn = last_action.typ == 'DEAL' and last_action.v1 == 'TURN'
                #identifies first river card state after swap
                AswapLogicTurn = numBoardCards == 4 and not can_discard
                #identifies showdown state
                showdown = numBoardCards == 5

                # goes to preflop logic file to get the new action
                for e in legalActions:
                    if e.typ == 'RAISE':
                        minRaise = int(e.v1)
                        maxRaise = int(e.v2)
                        break

                if preflop:
                    record.updatePreflopStats(button, lastActions)
                    action = prefL.getAction(lastActions, minRaise, maxRaise, bb, potSize, myBank, hole_odds)
                    s.send(action)
                
                #goes to flop before swap logic
                elif BswapLogicFlop:
                    record.updateFlopStats()
                    action = BSLF.getAction()
                    s.send(action)

                #goes to flop after swap logic
                elif AswapLogicFlop:
                    record.updateFlopStats()
                    action = ASLF.getAction()
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
