#!/usr/bin/env python3

# Use words.txt as the file name
fname = input("Enter file name: ")
with open(fname) as fh:
 for line in fh:
     print(line.upper().rstrip())
