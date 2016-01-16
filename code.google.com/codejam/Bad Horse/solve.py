#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
As the leader of the Evil League of Evil, Bad Horse has a lot of problems to deal with. Most recently, there have been far too many arguments and far too much backstabbing in the League, so much so that Bad Horse has decided to split the league into two departments in order to separate troublesome members. Being the Thoroughbred of Sin, Bad Horse isn't about to spend his valuable time figuring out how to split the League members by himself. That what he's got you -- his loyal henchman -- for. 
Input

 The first line of the input gives the number of test cases, T. T test cases follow. Each test case starts with a positive integer M on a line by itself -- the number of troublesome pairs of League members. The next M lines each contain a pair of names, separated by a single space. 
Output

 For each test case, output one line containing "Case #x: y", where x is the case number (starting from 1) and y is either "Yes" or "No", depending on whether the League members mentioned in the input can be split into two groups with neither of the groups containing a troublesome pair. 
Limits

 1 ≤ T ≤ 100.
 Each member name will consist of only letters and the underscore character.
 Names are case-sensitive.
 No pair will appear more than once in the same test case.
 Each pair will contain two distinct League members. 
Small dataset

 1 ≤ M ≤ 10. 
Large dataset

 1 ≤ M ≤ 100.

Sample:
<sample.txt>

Output:
Case #1: Yes
Case #2: No

Solution:
- dict graph: name -> [neighbours]
- dict color: name -> [0,1]
- find coloring of the graph
'''

import sys

def switch(c):
    return c ^ 1

def colorNeighbours(name, neighb, colors):
    c0 = colors[name]
    for n in neighb[name]:
      if n in colors:
         # already visited
         if (colors[n] == c0):
           # same color, we failed
           return False
      else:
        colors[n] = switch(c0)
        if not colorNeighbours(n, neighb, colors):
          return False
    return True
     
def solve(pairList):
    neighb = {}
    colors = {}
    # build graph
    for p in pairList:
      neighb.setdefault(p[0], set()).add(p[1])
      neighb.setdefault(p[1], set()).add(p[0])
    # color it
    for name in neighb:
     if not name in colors:
       colors[name] = 0
     if not colorNeighbours(name, neighb, colors):
       return False
    
    return True

def main():
    if len(sys.argv) < 2:
      print("missing filename")
      exit(1)
    with open(sys.argv[1],'r') as f:
      lines = [x.strip() for x in f.readlines()]
    
    testcases = int(lines.pop(0));
    
    for t in range(1,testcases+1):
      cnt = int(lines.pop(0))
      pairs = lines[:cnt]
      lines = lines[cnt:]
      res = solve([p.split() for p in pairs])
      print("Case #%i: %s" % (t, {False: 'No', True: 'Yes'}[res]))

if  __name__ =='__main__':
  main()


