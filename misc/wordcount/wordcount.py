#!/usr/bin/python3

import re
from sys import argv

if (len(argv) < 2):
 print("Missing argument")
 exit(1);

counts = {}

with open(argv[1]) as f:
  for line in f:
    for word in re.split(r'\W+', line):
       if word != '':
         word = word.lower()
         c = counts.get(word, 0);
         c += 1
         counts[word] = c

sortedcount = list(counts.items());
sortedcount.sort(key=lambda x:-x[1])


for (w,c) in sortedcount:
  print('%i\t%s' % (c, w))

