#!/usr/bin/env python3
import re

'''
Rock Paper Scissors game
opponent: a=rock, b=paper, c=scissors
part 1: x=rock, y=paper, z=scissors
part 2: x=lose, y=draw, z=win
'''

def read_input(final):
  if (final):
    fname = 'input'
  else:
    fname = 'input.sample'
  with open(fname, 'rt') as f:
    pat = re.compile('\\w')
    return [''.join(pat.findall(line)).lower() for line in f]

score1 = { 'ax': 1+3, 'ay': 2+6, 'az': 3+0,
           'bx': 1+0, 'by': 2+3, 'bz': 3+6,
           'cx': 1+6, 'cy': 2+0, 'cz': 3+3 }

score2 = { 'ax': 3+0, 'ay': 1+3, 'az': 2+6,
           'bx': 1+0, 'by': 2+3, 'bz': 3+6,
           'cx': 2+0, 'cy': 3+3, 'cz': 1+6 }

def solve(final):
  games = read_input(final)
  print(sum([score1[g] for g in games]))
  print(sum([score2[g] for g in games]))

if __name__ == '__main__':
 print("(expected:   15,  12)")
 solve(False)
 print('*'*30)
 print("(expected: 10310, 14859)")
 solve(True)
