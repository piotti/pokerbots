def getAction(lastActions, bb, potSize, minRaise, maxRaise, myBank):
    lastActionParts = lastActions[-1].split(':')
    raised = lastActionParts[0] == 'RAISE'
    if raised:
        amount = int(lastActionParts[1])
        ratio_bb = amount / bb
        ratio_pot = amount / potSize
    if hole_odds > 80:
        action = 'RAISE:'+str(0.5*potSize)+'\n'
        
    elif hole_odds > 70:
        raise_amount = min(max(minRaise, 0.5*potSize), maxRaise)
        if raise_amount / myBank <= .44:
            action = 'RAISE:'+str(raise_amount)+'\n'
            
        else:
             action = 'CALL\n'   
    elif good_hand:
        if raised:
            if ratio_bb <= 3:
                action = 'CALL\n'
            else:
                action = 'CHECK\n'
        else:
            action = 'CHECK\n'
                
    else:
        action = 'CHECK\n'
    return action