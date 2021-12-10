#!/usr/bin/env python3

'''
Verify input syntax (pairing of braces, parentheses, ...) and compute score based on number & type of errors.
'''

def read_input(final):
  if (final):
    fname = 'input'
  else:
    fname = 'input.sample'
  with open(fname, 'rt') as f:
    return [line.strip() for line in f]

def score(line):
   m = {'[':']', '{':'}', '(':')', '<':'>'}
   mr = {m[i]:i for i in m}
   s = {')':3, ']':57, '}':1197, '>':25137}
   exp = []
   for c in line:
     if c in m:
       exp.append(m[c])
     elif c in mr:
       if len(exp) == 0 or exp[-1] != c:
         return (s[c], 0)
       else:
         exp.pop()
     else:
       raise ValueError(line)
   if len(exp) == 0:
     raise ValueError('valid line', line)
   return (0, score2(exp))

def score2(exp):
  total = 0
  s = {')':1, ']':2, '}':3, '>':4}
  for c in exp[::-1]:
    total *= 5
    total += s[c]
  return total

def solve(final):
  lines = read_input(final)
  scores = [score(l) for l in lines]
  print('Part1', sum([s for (s,_) in scores]))
  
  scores2 = sorted([s2 for (_,s2) in scores if s2 > 0])
  print('Part2', scores2[len(scores2)//2])
  #print(s)
  #print(al)
  #print(lines)

if __name__ == '__main__':
 solve(False)
 solve(True)
