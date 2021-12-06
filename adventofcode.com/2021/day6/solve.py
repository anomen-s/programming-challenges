#!/usr/bin/env python3

'''
Simulate spawning of fish.
Each fish spawn a new one on 9th day and then each 7 days.
Input: for each fish number of days remaining to spawning
'''

def read_input(final):
  if (final):
    fname = 'input'
  else:
    fname = 'input.sample'
  with open(fname, 'rt') as f:
    return [int(n) for rawline in f for n in rawline.strip().split(',')]

def solve(final):
  init = read_input(final)
  # print(init)
  fish = [0] * 9
  for f in init:
    fish[f] += 1

  for _ in range(256 if final else 80):
    newf = fish[0]
    fish = fish[1:] + [newf]
    fish[6] += newf

  print(sum(fish))


if __name__ == '__main__':
 solve(False)
 solve(True)
