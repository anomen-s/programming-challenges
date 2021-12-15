#!/usr/bin/env python3
from collections import defaultdict

'''
Apply templates recursively
Part1: most/least common character after 10 iterations
Part2: most/least common character after 40 iterations
'''

def read_input(final):
  if (final):
    fname = 'input'
  else:
    fname = 'input.sample'
  with open(fname, 'rt') as f:
    content = [c.split('\n') for c in f.read().strip().split('\n\n')]
    d = dict([x.strip() for x in s.split('->')] for s in content[1])
    return (content[0][0], d)

def print_state(label, seed, template):
  totals = defaultdict(lambda: 0)
  totals[seed[0]] += 1
  totals[seed[-1]] += 1
  for pair in template:
    totals[pair[0]] += template[pair]
    totals[pair[1]] += template[pair]
  totals = [totals[pair]//2 for pair in totals]
  # print(totals)
  print(label, max(totals) - min(totals))

def solve(final):
  (seed, rules) = read_input(final)

  # print(seed)
  # print(rules)

  template = defaultdict(lambda: 0)
  for i in range(len(seed)-1):
    pair = seed[i]+seed[i+1]
    template[pair] += 1

  for s in range(40):
    state = template
    template = defaultdict(lambda: 0)
    for pair in state:
      pair1 = pair[0]+rules[pair]
      template[pair1] += state[pair]
      pair2 = rules[pair]+pair[1]
      template[pair2] += state[pair]

    if s == (10-1):
      print_state('Part1', seed, template)

  print_state('Part2', seed, template)


if __name__ == '__main__':
 solve(False)
 print('*' * 30)
 solve(True)
