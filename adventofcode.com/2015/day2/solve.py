#!/usr/bin/env python3

'''
Present wrapping.
Compute required amount of wrappng paper.
Compute required length of ribbon.
'''

def read_input(final):
  if (final):
    fname = 'input'
  else:
    fname = 'input.sample'
  with open(fname, 'rt') as f:
    return [[int(x) for x in line.strip().split('x')] for line in f]


def paper(l,w,h):
  dims = sorted([l,w,h])
  return 2*l*w + 2*w*h + 2*h*l + dims[0]*dims[1]

def ribbon(l,w,h):
  dims = sorted([l,w,h])
  return 2*dims[0] + 2*dims[1] + l*w*h

def solve(final):
  boxes = read_input(final)
  w = [paper(*b) for b in boxes]
  r = [ribbon(*b) for b in boxes]
  return [sum(w), sum(r)]

if __name__ == '__main__':
 print("(expected: %i, %i)" % ((58+43), (34+14)))
 print(solve(False))
 print('*'*30)
 print("(expected: %i, %i)" % (1586300, 3737498))
 print(solve(True))
