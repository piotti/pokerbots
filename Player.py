import argparse
import socket
import sys
import pickle
import preflopLogic as prefL
import BswapLogicFlop as BSLF


"""
Simple example pokerbot, written in python.

This is an example of a bare bones pokerbot. It only sets up the socket
necessary to connect with the engine and then always returns the same action.
It is meant as an example of how a pokerbot should communicate with the engine.
"""

FACE_VALS = ['2','3','4','5','6','7','8','9','T','J','Q','K','A']
PAIR_ODDS = [84.9, 82.12, 79.63, 77.15, 74.66, 71.67, 68.72, 65.73, 62.7, 59.64, 56.26, 52.84, 49.39][::-1]

class Player:
    def run(self, input_socket):
        # Get a file-object for reading packets from the socket.
        # Using this ensures that you get exactly one packet per read.
        f_in = input_socket.makefile()
        above_fifty = pickle.load(open('above_fifty.pkl', 'rb'))
        hole_odds_dict = pickle.load(open('odds.pkl', 'rb'))
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
                [handId, button, holeCard1, holeCard2, myBank, otherBank, timeBank] = parts[1:]
                handId = int(handId)
                button = bool(button)
                myBank = int(myBank)
                otherBank = int(otherBank)

                v1 = holeCard1[0]
                v2 = holeCard2[0]
                suited = holeCard1[1] == holeCard2[1]
                if FACE_VALS.index(v1) < FACE_VALS.index(v2):
                    good_hand = above_fifty[(v1+'/'+v2, suited)]
                    hole_odds = hole_odds_dict[(v1+'/'+v2, suited)]
                elif FACE_VALS.index(v1) > FACE_VALS.index(v2):
                    good_hand = above_fifty[(v2+'/'+v1, suited)]
                    hole_odds = hole_odds_dict[(v2+'/'+v1, suited)]
                else:
                    good_hand = FACE_VALS.index(v1) > 0
                    hole_odds = PAIR_ODDS[FACE_VALS.index(v1)]


                print hole_odds


            elif word == "GETACTION":

                [potSize, numBoardCards] = [int(e) for e in parts[1:3]]
                boardCards = parts[3:3+numBoardCards]
                numLastActions = int(parts[3+numBoardCards])
                lastActions = parts[4+numBoardCards:4+numBoardCards+numLastActions]
                numLegalActions = int(parts[4+numBoardCards+numLastActions])
                legalActions = parts[5+numBoardCards+numLastActions:5+numBoardCards+numLastActions+numLegalActions]

                #indentifies preflop state
                preflop = numBoardCards == 0
                #identifies flop before swap state
                BswapLogicFlop = numBoardCards == 3
                #identigies flop after swap state
                AswapLogicFlop = numBoardCards == 3
                #identifies first river card state before swap
                BswapLogicRiver = numBoardCards == 4
                #identifies first river card state after swap
                AswapLogicRiver = numBoardCards == 4

                #identifies showdown state
                showdown = numBoardCards == 5

                for e in legalActions:
                    parts = e.split(':')
                    if parts[0] == 'RAISE':
                        minRaise = int(parts[1])
                        maxRaise = int(parts[2])
                        break

                # goes to preflop logic file to get the new action
                if preflop:
                    action = prefL.getAction(lastActions, bb, potSize, minRaise, maxRaise, myBank)
                    s.send(action)
                
                #goes to flop before swap logic
                elif BswapLogic:
                    action = BSLF.getAction()
                    s.send(action)

                #goes to flop after swap logic
                elif AswapLogic:
                    action

                #goes to 4th card before swap logic
                elif BswapLogicRiver:

                #goes to 4th card after swap logic
                elif AswapLogicRiver:

                #goes to showdown logic
                else:
                    if good_hand:
                        s.send('CALL\n')
                    else:
                        s.send('CHECK\n')

                
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
