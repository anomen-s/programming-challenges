#!/usr/bin/python3
# -*- coding: utf-8 -*-

import calendar

def main():
  MONTHS = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
  
  d1 = 2 # Tuesday
  c = 0
  
  for year in range(1901, 2001):
    if calendar.isleap(year):
      MONTHS[1] = 29
    else:
      MONTHS[1] = 28
    
    for month in range(12):
      if (d1 == 0):
        c = c+1
        print([c, 'month after:', year, month])
      d1 = (d1 + MONTHS[month]) % 7
     
  print (c)
    
if  __name__ =='__main__':main()
