#!/usr/bin/env python3
from math import *

def compute(cell):
 # side of rectangle
 root = ceil(sqrt(cell))
 if (root % 2) == 0:
   root = root + 1
 # layer, indexed from 0
 layer = root // 2
 
 # index of last item of prev layer
 layer_start = (root-2)**2
 # index of last item i the layer
 layer_end = root**2
 
 seglen=(layer_end - layer_start) // 4
 for seg in range(4):
   sstart = layer_start + seglen*seg
   send = layer_start + seglen*(seg + 1)
   if (send >cell):
     smid = layer_start + int(seglen * (seg + 0.5))
     return layer + abs(smid-cell)


# cell number, indexed from 1
cell = int(input())
print(compute(cell))

