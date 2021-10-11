name = input("Enter file:")
if len(name) < 1 : name = "mbox-short.txt"
handle = open(name)
stats = {}
for line in handle:
    l = line.rstrip().split(' ')
    if l[0] == 'From':
        #print(line)
        hour = l[6].split(':')[0]
        stats[hour] = stats.get(hour, 0) + 1

for h in sorted(stats.items()):
    print(*h)
    
    
        
