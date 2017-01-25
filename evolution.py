import random
import json
import gradDescent

winners = [int(e) for e in open('winners.txt', 'r').readlines()]
paramList = json.loads(open('params.txt', 'r').read())


w = winners[-1]
l = w+1 if w%2==0 else w-1
paramList[l][0] = gradDescent.newParam(paramList[w][0], paramList[l][0], False)

f = open('params.txt', 'w')
f.write(json.dumps(paramList))
f.close()


