#!/usr/bin/env python3
import re

'''
Play dice game
'''

def read_input(final):
  if (final):
    fname = 'input'
  else:
    fname = 'input.sample'
  with open(fname, 'rt') as f:
    content = [c.strip() for c in f]
    lines = [re.match('Player (\\d+) starting position: (\\d+)\\s*', line) for line in content]
    return {m[1]: int(m[2]) for m in lines}

def modn(val, maxval):
    '''
    Perform modulo on range 1..maxval.
    '''
    return ((val-1) % maxval) + 1

class Dice:
   def __init__(self, max_val):
      self.m = max_val
      self.n = 1
      self.r = 0

   def __next__(self):
      result = self.n
      self.r += 1
      if result == self.m:
        self.n = 1
      else:
        self.n += 1
      return result

   def next3(self):
      return sum([next(self) for _ in range(3)])

   def rolls(self):
      return self.r


def solve(final):
 start = read_input(final)
 print('start', start)

 p1 = [start['1'], 0]
 p2 = [start['2'], 0]
 dice = Dice(100)
 players = [p1, p2]

 while players[1][1] < 1000:
   p = players[0]
   roll = dice.next3()
   p[0] = modn(p[0] + roll, 10)
   p[1] += p[0]

   players = players[::-1]

 print('Part1', min(p1[1], p2[1]) * dice.rolls())


if __name__ == '__main__':
 solve(False)
 print('*' * 30)
 solve(True)
