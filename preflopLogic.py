import random
def getAction(lastActions, minRaise, maxRaise, bb, potSize, myBank, hand, hole_odds, p_all_in_t, p_raise_t, p_call_t_one, p_call_t_two, p_bluff):
    rand = random.random()
    ranks = []
    AorK = False
    st = []
    for card in hand:
        st.append((card.fv, card.suit))
        if card.fv == 'A' or card.fv == 'K':
            AorK = True

    raised = lastActions[-1].typ == 'RAISE'
    raise_amount = min(max(minRaise, 0.5*potSize), maxRaise)
    ratio_bb = 0
    if raised:
        amount = lastActions[-1].amount
        ratio_bb = amount / bb
        ratio_pot = amount / potSize
       

    if hole_odds > p_all_in_t:
        return 'RAISE:'+str(raise_amount)+'\n'
        
    #elif hole_odds > 60 or rand < .06: 
    elif hole_odds > p_raise_t or rand < p_bluff:
        if raise_amount / (200-(potSize/2)) <= .5:
            return 'RAISE:'+str(raise_amount)+'\n'
        else:

            return 'CALL\n'
    else:
        if raised:
            if ratio_bb <= p_call_t_one and ratio_bb != 0:
            #if ratio_pot < 2: 
                return 'CALL\n'
            elif AorK and ratio_bb <= p_call_t_two and ratio_bb != 0:
            #elif AorK:
                return 'CALL\n'
            else:
                return 'CHECK\n'    
        else:
            if AorK:
                return 'RAISE:' +str(raise_amount)+'\n'
            return 'CALL\n'
   