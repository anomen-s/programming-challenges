#!/usr/bin/python
# -*- coding: utf-8 -*-
# Work out the first ten digits of the sum of the following one-hundred 50-digit numbers.

def readfile(filename):
    f = open(filename)
    try:
       data = f.read(6000)
    finally:
       f.close()
    return data.split()


S = 0
for i in readfile('numbers.txt'):
    print S
    S = S + int(i)

print 'sum', S
print '10digits', str(S)[0:10]


