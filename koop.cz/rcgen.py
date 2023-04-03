#!/usr/bin/env python3

def print_rc(y,m,d,n):
    odd = y//10 + m//10 + d//10 + n//100 + n%10
    even = y%10 + m%10 + d%10 + (n//10)%10
    c = (odd - even + 11*11) % 11
    if c < 10:
      print('%02d%02d%02d%03d%d' % (y, m, d, n, c))

def gen(from_year, to_year):
  for yr in range(from_year-1900, to_year-1900):
    y = yr%100
    for m in range(1,13):
      for d in range(1,32):
        for n in range(1000):
          # M
          print_rc(y,m,d,n)
          # F
          print_rc(y,m+50,d,n)
          # new additional ranges
          #print_rc(y,m+20,d,n)
          #print_rc(y,m+50+20,d,n)


gen(1950, 2020)

