#!/usr/bin/python3
# -*- coding: utf-8 -*-

def triangle(n):
    return n * (n+1) // 2

def pentagonal(n):
    return n * (3*n - 1) // 2

def hexagonal(n):
    return n * (2*n - 1)
    

def test():
    r = 40755
    r3 = triangle(285)
    r5 = pentagonal(165)
    r6 = hexagonal(143)
    assert (r == r3)
    assert (r == r5)
    assert (r == r6)
    

def main():
    test()
    t = [1,1]
    p = [1,1]
    h = [1,1]
    for z in range(10**6):
      n = t[0] + 1
      t[0] = n
      t[1] = triangle(n)
      while p[1] < t[1]:
        n = p[0] + 1
        p[0] = n
        # p[1] = pentagonal(n)
        p[1] = p[1] + 3*(n-1) + 1 # minor optimization
      while h[1] < t[1]:
        # inc h
        n = h[0] + 1
        h[0] = n
        # h[1] = hexagonal(n)
        h[1] = h[1] + 4 * (n-1) + 1 # minor optimization
      if t[1] == p[1] == h[1]:
        print(t)

if  __name__ =='__main__':main()
