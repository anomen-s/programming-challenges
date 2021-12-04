#!/usr/bin/env python3

'''
Find most/least common bit values and create new values.
'''

def higher_bit(a):
  if a[0] > a[1]:
    return '0';
  if a[0] < a[1]:
    return '1'
  raise ValueError(a)

def lower_bit(a):
  return higher_bit(a[::-1])

max_len = 0

with open('input', 'rt') as f:
    for rawline in f:
      max_len = max(max_len, len(rawline.strip()))

# value frequencies
cnt = [[0, 0] for i in range(max_len)]

with open('input', 'rt') as f:
    for rawline in f:
      line = rawline.strip()
      for i in range(0, len(line)):
        # print(line[i])
        val = int(line[i])
        # print(i, val, line)
        cnt[i][val] = cnt[i][val] + 1

s_gamma = [higher_bit(x) for x in cnt]
s_epsilon = [lower_bit(x) for x in cnt]

gamma = int(''.join(s_gamma), 2)
epsilon = int(''.join(s_epsilon), 2)

#print(cnt, s_gamma, s_epsilon, gamma, epsilon)

print(gamma * epsilon)
