import sys
import math

# Don't let the machines win. You are humanity's last hope...

width = int(input())  # the number of cells on the X axis
height = int(input())  # the number of cells on the Y axis
grid = []
results = []
for i in range(height):
    line = input()  # width characters, each either 0 or .
    grid.append(line)
    results.append([[-1]*4 for x in range(width)])

# find right neighbour
for r in range(height):
    gr = grid[r]
    lastnode = -1
    for c in range(width-1, -1, -1):
        if gr[c] == '0':
            if lastnode != -1:
                results[r][c] = [lastnode, r, -1, -1] 
            lastnode = c

#print(results, file=sys.stderr)

#print("%s" % (results[r][c]), file=sys.stderr)

# find bottom neighbour
for c in range(width):
    lastnode = -1
    for r in range(height-1, -1, -1):
        if grid[r][c] == '0':
            if lastnode != -1:
                results[r][c][2] = c
                results[r][c][3] = lastnode
            lastnode = r
            #print("%i %i %s" % (c,r,results[r][c]), file=sys.stderr)
            print(" ".join(map(lambda x: str(x), [c,r] + results[r][c])))
            

# Write an action using print
# To debug: print("Debug messages...", file=sys.stderr)


# Three coordinates: a node, its right neighbor, its bottom neighbor
#print("0 0 1 0 0 1")
#print("1 0 -1 -1 -1 -1")
#print("0 1 -1 -1 -1 -1")

