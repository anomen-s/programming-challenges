#!/usr/bin/env python3

with open('input', 'r') as f:
   data = f.readlines()
   data = [[int(d) for d in l.split()] for l in data]
   sums = [max(l) - min(l) for l in data]
   print(sum(sums))
