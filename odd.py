import pickle

f = open('hole_odds.txt')
cards = ['2', '3','4','5','6','7','8','9','T','J','Q','K','A']
odds_pickle = {}
for l in f.readlines():
        parts = l.split()
        parts = [p for p in parts if p]
        combo = parts[0]
        suited = parts[1]=='suited'
        odds = float(parts[2][:-1])
        odds_pickle[(combo, suited)] = odds

file_ = open('odds.pkl', 'wb')
pickle.dump(odds_pickle, file_, pickle.HIGHEST_PROTOCOL)
file_.close()

#af = pickle.load(open('above_fifty.pkl', 'rb'))
