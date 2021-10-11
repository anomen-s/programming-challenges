name = input("Enter file:")
if len(name) < 1 : name = "mbox-short.txt"
handle = open(name)
senders = {}
for line in handle:
    l = line.rstrip().split(' ')
    if l[0] == 'From':
      sender = l[1]
      senders[sender] = senders.get(sender, 0) + 1

maxC = 0
maxN = ''
for name in senders:
    if senders[name] > maxC:
        maxC = senders[name]
        maxN = name

print(maxN, maxC)
