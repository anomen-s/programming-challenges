import sys
import math

'''
A finance company is carrying out a study on the worst stock investments and would like to acquire a program to do so.
The program must be able to analyze a chronological series of stock values in order to show the largest loss that it is possible to make by buying a share at a given time t0 and by selling it at a later date t1.
The loss will be expressed as the difference in value between t0 and t1.
If there is no loss, the loss will be worth 0.
'''

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.


maxVal = -2**30
maxDiff = 0
n = int(input())
for i in input().split():
    v = int(i)
    if v > maxVal:
        maxVal = v
    else:
        currDiff = v - maxVal
        if currDiff < maxDiff:
            maxDiff = currDiff

# Write an action using print
# To debug: print("Debug messages...", file=sys.stderr)

print(maxDiff)

