
'''
The Goal
The goal for your program is to make a motorbike jump across a gap and land on a platform then stop.
  Rules

The platform is located on the otherside of a gap in the road above a chasm. The lengths of the road, gap and platform are measured in cells.
 

At the start of the program, you are given:

    The variable road: the length of the road before the gap.
    The variable gap: the length of the gap.
    The variable platform: the length of the platform.

At the start of each game turn, the motorbike gives you:

    The variable speed: its ocurrent speed.
    The variable coordX: its position on the road.

The motorbike's initial position is coordX = 0. It always moves in a straight line. At the end of each turn, it moves forward a number of spaces equal to its speed (speed). For example, if coordX = 1 and speed = 3, coordX will be 4 at the next turn. The bike can start with any speed, including being at a stop.
 

Before the end of the turn, you must output one of the following commands:

    SPEED: increases the speed of the motorbike by 1 (+1 to the speed variable).
    SLOW: decreases the speed of the motorbike by 1 (-1 to the speed variable).
    JUMP: makes the motorbike jump.
    WAIT: does nothing (the motorbike keeps the same speed).
'''

import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

road = int(input())  # the length of the road before the gap.
gap = int(input())  # the length of the gap.
platform = int(input())  # the length of the landing platform.

print(['in', road,gap,platform], file=sys.stderr)

L = road+gap+platform
T = [[]] * L
pstart = road+gap

def is_valid(T, pos, speed):
  if len(T) <= pos:
    return False
  t0 = T[pos]
  if len(t0) <= speed:
    return False
  #print([t0, speed,len(t0)], file=sys.stderr)
  return (type(t0[speed]) == str) and (t0[speed] != '')
  

# compute table for platform
for idx in range(platform-1,-1,-1):
  maxspeed = 2
  for speed in range (1, platform-idx+1):
    #print(['test',idx,speed], file=sys.stderr)
    #print(['test ->',pstart+idx+speed, speed-1], file=sys.stderr)
    if is_valid(T, pstart+idx+speed, speed-1):
        maxspeed = maxspeed + 1
  T[pstart+idx] = ['SLOW'] * maxspeed
  print(['set',pstart+ idx, T[pstart+idx]], file=sys.stderr)

# compute table for road
for idx in range(road-1,-1,-1):
  T[idx] = [''] * (L-idx)
  for speed in range(L-idx):
    T[idx][speed] = "";
    next_pos = idx+speed
    #print(['compute', idx, speed,next_pos, T[idx]], file=sys.stderr)
    if is_valid(T, next_pos, speed):
      if next_pos <= road:
        T[idx][speed] = "WAIT";
      else:
        T[idx][speed] = "JUMP";
      
    if ((next_pos-1) < road) and (speed>0) and is_valid(T, next_pos-1, speed-1):
      T[idx][speed] = "SLOW";
    if ((next_pos+1) < road) and is_valid(T, next_pos+1, speed+1):
      T[idx][speed] = "SPEED";
  print(['set', idx, T[idx]], file=sys.stderr)


# dynamic programming
# T is table: <pos> * <speed> -> <Action>

# game loop
while True:
    speed = int(input())  # the motorbike's speed.
    coord_x = int(input())  # the position on the road of the motorbike.

    if coord_x >= len(T):
      print(['ko1', speed, coord_x], file=sys.stderr)
      break
    t0 = T[coord_x]
    if speed >= len(t0):
      print(['ko2', speed, coord_x], file=sys.stderr)
      break
    action = t0[speed]

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)

    # A single line containing one of 4 keywords: SPEED, SLOW, JUMP, WAIT.
    print(action)

    if (speed == 0) and (pstart < coord_x):
      break
