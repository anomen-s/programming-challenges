#!/usr/bin/env python3

'''
Bingo.
Find score of the last winning board.
'''

def read_input(final):
  if (final):
    fname = 'input'
  else:
    fname = 'input.sample'
  with open(fname, 'rt') as f:
    return iter([rawline.strip() for rawline in f])

def next_block(lines):
   result = []
   while True:
     try:
      line = next(lines)
      if line == '':
        raise StopIteration
     except StopIteration as stop:
      if result == []:
        raise stop
      else:
        return result
     result.append(line)

class Board:

    def __init__(self, rows):
        self.rows = [[int(i) for i in r.split()] for r in rows]

    def __repr__(self):
        return 'Board{' + str(self.rows) + '}'

    def iswinning(self, draw):
        return self.haswinningrow(draw) or self.haswinningcol(draw)

    def haswinningrow(self, draw):
        rsums = [sum([1 for c in r if c in draw]) for r in self.rows]
        return max(rsums) == 5

    def haswinningcol(self, draw):
        for c in range(5):
          col = [self.rows[r][c] for r in range(5)]
          if sum([1 for i in col if i in draw]) == 5:
           return True
        return False

    def score(self, draw):
        if not self.iswinning(draw):
          return -1
        return sum([c for r in self.rows for c in r if c not in draw]) * draw[-1]

def load(final):
  lines = read_input(final)
  # print(list(lines))
  draw = [int(n) for n in next_block(lines)[0].split(',')]
  # print (draw)
  boards = []
  try:
   while True:
    boards.append(Board(next_block(lines)))
  except StopIteration:
    # print(boards)
    pass
  return (draw, boards)

def solve(final):
  (draw, boards) = load(final)

  win_boards = [-1 for i in boards]
  last_win = -1

  for cnt in range(len(draw)):
    d = draw[:cnt]
    scores = [b.score(d) for b in boards]
    for b in range(len(boards)):
      if (scores[b] >= 0) and (win_boards[b] == -1):
        win_boards[b] = last_win = scores[b]
    # print('\t'.join([str(s) for s in scores]))

  print(last_win)

if __name__ == '__main__':
 solve(False)
 solve(True)
