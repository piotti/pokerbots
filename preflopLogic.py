
def getAction(lastActions, minRaise, maxRaise, bb, potSize, myBank, hand, hole_odds):
    ranks = []
    AorK = False
    st = []
    for card in hand:
        st.append((card.fv, card.suit))
        if card.fv == 'A' or card.fv == 'K':
            AorK = True

    last_action = lastActions[-1]
    raised = last_action.typ == 'RAISE'
    raise_amount = min(max(minRaise, 0.5*potSize), maxRaise)
    ratio_bb = 0
    if raised:
        amount = last_action.amount
        ratio_bb = amount / bb
        ratio_pot = amount / potSize
       

    if hole_odds > 70:
        print 'raised!', st
        return 'RAISE:'+str(raise_amount)+'\n'
        
    elif hole_odds > 60: 
        if raise_amount / myBank <= .44:
            print 'raised!', st
            return 'RAISE:'+str(raise_amount)+'\n'
        else:

            return 'CALL\n'
    else:
        if raised:
            if ratio_bb <= 3 and ratio_bb != 0:
                return 'CALL\n'
            elif AorK and ratio_bb <= 5 and ratio_bb != 0:
                return 'CALL\n'
            else:
                return 'CHECK\n'    
        else:
            return 'CALL\n'
   