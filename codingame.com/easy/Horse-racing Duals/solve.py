import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

n = int(input())
P = []
for i in range(n):
    pi = int(input())
    P.append(pi)


P.sort()
Dl = [(P[x]-P[x-1]) for x in range(1, len(P))]

# Write an action using print
# To debug: print("Debug messages...", file=sys.stderr)

print(min(Dl))

