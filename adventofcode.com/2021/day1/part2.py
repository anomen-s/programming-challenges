#!/usr/bin/env python3

'''
Count all sums of 3 consecutive values which are higher than is sum of 3 values starting on previous.
'''

prev = None
cnt = 0

buffer = []

with open('input', 'rt') as f:
    for rawline in f:
      line = int(rawline.strip())
      buffer.append(line)
      if len(buffer) >= 4:
        if sum(buffer[0:3]) < sum(buffer[1:4]):
        #  print(sum(buffer[0:3]), sum(buffer[1:4]), buffer[0:3], buffer[1:4])
          cnt = cnt + 1
        #else:
        #  print('nope', buffer[0:3], buffer[1:4])
        del(buffer[0])

print(cnt)
