#!/usr/bin/env python3
import math

'''
Part1: Count paths from start to end. Small caves (lowercase) visited at most once.
Part2: Count paths from start to end. One small cave (lowercase) can be visited twice, other small at most once.
'''

class Cave:
    def __init__(self, name):
      self.name = name
      self.n = []

    def __repr__(self):
      return self.name+'{'+str([x.name for x in self.n])+'}'

    def add(self, neighbour):
      self.n.append(neighbour)

    def issmall(self):
      return self.name != 'start' and self.name == self.name.lower()

    def visited(self, path):
      if self.name == 'start':
        return True
      # only check small caves and start (lowercase names)
      return self.issmall() and self.name in path


def read_input(name):
  if (name):
    fname = 'input.' + name
  else:
    fname = 'input'
  caves = {}
  with open(fname, 'rt') as f:
    for line in f:
      (c1,c2) = line.strip().split('-')
      if not c1 in caves:
        caves[c1] = Cave(c1)
      if not c2 in caves:
        caves[c2] = Cave(c2)
      caves[c1].add(caves[c2])
      caves[c2].add(caves[c1])
    return caves

def search(path, cave, paths, revisit):

  if cave.name == 'end':
    paths.add(','.join(path))
  else:
    for neigh in cave.n:
      if not neigh.visited(path):
        search(path + [neigh.name], neigh, paths, revisit)
      elif revisit and path[0] == 'start' and neigh.name != 'start':
        new_path = ['xstart'] + path[1:] + [neigh.name]
        search(new_path, neigh, paths, revisit)

def solve(name, revisit):
  caves = read_input(name)
  # print(caves)
  paths = set()

  search(['start'], caves['start'], paths, revisit)

  # for p in paths: print(p)
  # print(paths)
  print('Part2' if revisit else 'Part1', name, len(paths))


if __name__ == '__main__':
 solve('tiny', False)
 solve('sample', False)
 solve('larger', False)
 solve('', False)

 solve('tiny', True)
 solve('sample', True)
 solve('larger', True)
 solve('', True)
