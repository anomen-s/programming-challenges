import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ?'

l = int(input())
h = int(input())
t = input()
rows = []
for i in range(h):
    rows.append(input())

posList = []

for c in t:
    p = ALPHABET.find(c.upper())
    if (p < 0):
      p = len(ALPHABET)-1
    posList.append(p)

    
# Write an action using print
# To debug: print("Debug messages...", file=sys.stderr)

for r in rows:
  res = ''
  for p in posList:
      st = p * l
      res = res + r[st:st+l]
  print(res)
