#!/usr/bin/python3
from random import randint
from functools import reduce
'''
Suppose you're on a game show, and you're given the choice of three doors: 
Behind one door is a car; behind the others, goats. 
You pick a door, say No. 1, and the host, who knows what's behind the doors, opens another door, say No. 3, 
which has a goat. He then says to you, "Do you want to pick door No. 2?" Is it to your advantage to switch your choice?
'''


def test_ignoring(i = 0):
  '''
   Select door in first try
  '''
  choices = set([0,1,2])
  hit = randint(0, 2)
  guess1 = randint(0,2)
  if hit == guess1:
    return 'hit'
  else:
    return 'miss'

    

def test_hinted(i = 0):
  '''
    Change selection to last door (not selected in first try and not open).
  '''
  choices = set([0,1,2])
  hit = randint(0, 2)
  guess1 = randint(0,2)
  
  choices.remove(hit)
  opened = next(iter(choices ^ set([hit, guess1])))

  if guess1 == hit:
    return 'miss'
  else:
    return 'hit'


def incval(values, value):
  '''
    Updates dictionary with counts and returns the dictionary.
  '''
  c = values.get(value, 0)
  c += 1
  values[value] = c
  return values

  
print("Change selection to remaining door:")
print(reduce(incval,  map(test_hinted, range(10000)), dict()))

print("Select door originally selected:")
print(reduce(incval,  map(test_ignoring, range(10000)), dict()))
