import json
import sys

f = open('gamelog.txt', 'r')
line = f.readlines()[-1]
score = int(line.split()[2][1:-1])

params = json.loads(open('params.txt', 'r').read())

f = open('winners.txt', 'a')
p1 = int(sys.argv[1])
f.write(str(p1 if score > 0 else p1+1) +'\n')
f.close()
