#!/usr/bin/env python3

files = {}

print('open out...')

hexChars = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']

for i in range(0, 0x10):
  idx = hexChars[i]

  files[idx] = open(('pwned-%x.txt'%i), 'wt')

print('open in...')

c = 0
with open('pwned-passwords-sha1-ordered-by-hash-v4.txt') as pwnf:
    for line in pwnf:
      first = line[0]
      f = files[first]
      f.write(line)
      c=c+1
      if (c % 1000000) == 0:
        print(c)

print('closing')

for i in range(0, 0x10):
  idx = hexChars[i]
  files[idx].close()
