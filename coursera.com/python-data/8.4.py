fname = input("Enter file name: ")
fh = open(fname)
words = list()
for line in fh:
   #print(line.rstrip())
   for w in line.rstrip().split(' '):
     if w not in words:
       words.append(w)

print(sorted(words))
