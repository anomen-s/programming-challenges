import sys
import math

'''
The Goal
Destroy the mountains before your starship collides with one of them. For that, shoot the highest mountain on your path.
  Rules
At the start of each game turn, you are given the height of the 8 mountains from left to right.
By the end of the game turn, you must fire the highest mountain by outputting its index (from 0 to 7).

Firing on a mountain will only destroy part of it, reducing its height. Your ship descends after each pass.  
'''

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.


# game loop
while True:
    maxh = -1
    maxi = 0
    for i in range(8):
        mountain_h = int(input())  # represents the height of one mountain, from 9 to 0.
        #print("Debug messages..." + str(mountain_h), file=sys.stderr)
        if maxh < mountain_h:
              #print([mountain_h,i,maxh,maxi], file=sys.stderr)
              maxh = mountain_h
              maxi = i
  
    # Write an action using print

    # The number of the mountain to fire on.
    print(maxi)
