import random
import json

winners = [int(e) for e in open('winners.txt', 'r').readlines()]
paramList = json.loads(open('params.txt', 'r').read())

for i in range(50):
	w = winners[i]
	l = w+1 if w%2==0 else w-1
	for param in paramList[w]:
		mu = paramList[w][param]
		paramList[l][param] = max(2*mu/5, min(random.gauss(mu, mu/5), 8*mu/5))

random.shuffle(paramList)
f = open('params.txt', 'w')
f.write(json.dumps(paramList))
f.close()


