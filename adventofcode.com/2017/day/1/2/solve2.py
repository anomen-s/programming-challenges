#!/usr/bin/env python3

def csum(a):
   if a[0] == a[1]:
     return int(a[0])
   else:
     return 0

with open('input', 'r') as f:
   data = f.read().strip()
   shift = len(data) // 2
   seq = zip(data, data[shift:] + data[0:shift])
   print(sum([csum(a) for a in seq]))
