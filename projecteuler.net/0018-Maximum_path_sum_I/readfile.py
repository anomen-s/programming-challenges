#!/usr/bin/python
# -*- coding: utf-8 -*-

def readfile(filename):
    f = open(filename)
    try:
       data = f.readlines()
    finally:
       f.close()
    return map(lambda x : map(int, x.split()), data)

print readfile('data.txt')

