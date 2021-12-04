#!/usr/bin/env python3

'''
Find value by comparing with most/least common bit values.
'''

def most_common_bit(a):
  return '0' if (a[0] > a[1]) else '1'

def least_common_bit(a):
  return '1' if (a[0] > a[1]) else '0'

def read_input(final):
  if (final):
    fname = 'input'
  else:
    fname = 'input.sample'
  with open(fname, 'rt') as f:
    return [rawline.strip() for rawline in f]

def max_len(lines):
  return max([len(l) for l in lines])

def count_by_index(lines, idx):
  '''
  return list of counts of digits at given index
  '''
  cnt = [0, 0]
  for l in lines:
     val = int(l[idx])
     cnt[val] = cnt[val] + 1
  return cnt


def filter_by_index(lines, idx, value_selector):
  # find digit occurences at given index
  occur = count_by_index(lines, idx)
  # select which digit value should be retained
  filter_by = value_selector(occur)
  # filter by found value (or 1 if equal)
  return [l for l in lines if l[idx] == filter_by]
  # return list(filter(lambda l: l[idx] == filter_by, lines))

def find_val(all_lines, value_selector):
  '''
  find row matching values given by value_selector
  '''
  lines = all_lines
  for i in range(0, max_len(all_lines)):
     lines = filter_by_index(lines, i, value_selector)
     if len(lines) == 1:
       return lines[0]
  raise ValueError

def solve(final):
  lines = read_input(final)
  # print(filter_by_index(lines, 0, most_common_bit))
  oxy = int(find_val(lines, most_common_bit), 2)
  co2 = int(find_val(lines, least_common_bit), 2)
  #print(oxy, co2)
  print(oxy * co2)

if __name__ == '__main__':
 solve(False)
 solve(True)
