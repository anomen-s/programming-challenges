#!/usr/bin/env python3

def csum(a):
   if a[0] == a[1]:
     return int(a[0])
   else:
     return 0

with open('input', 'r') as f:
   data = f.read().strip()
   seq = zip(data, data[1:] + data[0:1])
   print(sum([csum(a) for a in seq]))
