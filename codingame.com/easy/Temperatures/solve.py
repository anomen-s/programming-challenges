import sys
import math
'''
Write a program that prints the temperature closest to 0 among input data.
If two numbers are equally close to zero, 
positive integer has to be considered closest to zero
(for instance, if the temperatures are -5 and 5, then display 5).
'''

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

n = int(input())  # the number of temperatures to analyse
temps = input()  # the n temperatures expressed as integers ranging from -273 to 5526

# Write an action using print
# To debug: print("Debug messages...", file=sys.stderr)


if n > 0:
 temps = [int(x) for x in temps.split(' ')]
 print(temps, file=sys.stderr)
 tmin = temps[0]
 amin = abs(tmin)
 for i in temps[1:]:
     ai = abs(i)
     if (ai < amin):
         (tmin, amin) = (i, ai)
     elif (ai == amin) and (i > 0):
         (tmin, amin) = (i, ai)

 print(tmin)
else:
  print("0")

