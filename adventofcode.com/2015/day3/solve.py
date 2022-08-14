#!/usr/bin/env python3

'''
Travelling on 2-D map.
Compute visited points when following all movent instructions.
Compute visited points, if two santas takes turns in movement.
'''

def read_input(final):
  if (final):
    fname = 'input'
  else:
    fname = 'input.sample'
  with open(fname, 'rt') as f:
    lines = [l for l in f]
    return lines[0]


def compute(moves):
  p = (0,0)
  points = set()
  points.add(p)

  for i in range(len(moves)):
    m = moves[i]
    if m == '^':
      p = (p[0], p[1]+1)
    elif m == 'v':
      p = (p[0], p[1]-1)
    elif m == '<':
      p = (p[0]-1, p[1])
    elif m == '>':
      p = (p[0]+1, p[1])

    points.add(p)

  return points


def solve(final):
  moves = read_input(final)

  part1 = compute(moves)

  part2a = compute(moves[::2])
  part2b = compute(moves[1::2])
  part2 = set.union(part2a, part2b)

  return [len(part1), len(part2)]

if __name__ == '__main__':
 print("(expected: %i, %i)" % (4, 3))
 print(solve(False))
 print('*'*30)
 print("(expected: %i, %i)" % (2572, 2631))
 print(solve(True))
