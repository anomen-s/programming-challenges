#!/usr/bin/env python3

'''
Count all values which are higher then previous value.
'''

prev = None
cnt = 0

with open('input', 'rt') as f:
    for rawline in f:
      line = int(rawline.strip())
      # print(line)
      if (prev != None) and (line > prev):
        cnt = cnt + 1
      prev = line

print(cnt)
