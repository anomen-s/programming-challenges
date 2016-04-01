import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

n = int(input())  # Number of elements which make up the association table.
q = int(input())  # Number Q of file names to be analyzed.
db = {}
for i in range(n):
    # ext: file extension
    # mt: MIME type.
    ext, mt = input().split()
    print([ext, mt], file=sys.stderr)
    db[ext.lower()] = mt
    
for i in range(q):
    fname = input()  # One file name per line.
    print([fname], file=sys.stderr)

    pos = fname.rfind('.')
    if pos >= 0:
      ext = fname[pos+1:].lower()
      print(db.setdefault(ext, 'UNKNOWN'))
    else:
        print('UNKNOWN')
# Write an action using print
# To debug: print("Debug messages...", file=sys.stderr)

# For each of the Q filenames, display on a line the corresponding MIME type. If there is no corresponding type, then display UNKNOWN.
#print("UNKNOWN")
