#!/usr/bin/env python3

'''
Elevator (up/down). When it goes underground for the first time?
'''

def read_input(final):
  if (final):
    fname = 'input'
  else:
    fname = 'input2.sample'
  with open(fname, 'rt') as f:
    c = [line.strip() for line in f]
    return c[0]


def solve(final):
  r = read_input(final)
  f = 0
  
  for i in range(len(r)):
    if r[i] == '(':
      f+=1
    elif r[i] == ')':
      f-=1
    else:
      raise Exception('Unexpected char ' + r[i])
    if f < 0:
      return i+1 # index of first char is 1

  raise Exception('Never reached')

if __name__ == '__main__':
 print("(expected: 5)")
 print(solve(False))
 print('*'*30)
 print("(expected: 1797)")
 print(solve(True))
