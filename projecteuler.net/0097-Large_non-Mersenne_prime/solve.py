#!/usr/bin/python3
# -*- coding: utf-8 -*-


import math

Coef = 28433
Power = 7830457
Add = 1


Cycle = 4*5**(10-1)

def main():
    global Power, Coef,Add, Cycle
    c = 0
    res = 1
    while Power > Cycle:
       Power = Power - Cycle
       print('reduce exponent by 1 cycle to ' + str(Power))

#    res = (2 ** Power) % (10**10)

    for i in range(Power):
      res = res * 2
      c = c + 1
      # reduce number of modulos
      if c > 10:
        c = 0
        res = res % (10**10)

    res = (res * Coef  + Add) % (10**10)
          

    print(res)
    
if  __name__ =='__main__':main()
