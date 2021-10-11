# Use the file name mbox-short.txt as the file name
fname = input("Enter file name: ")
fh = open(fname)
val = 0
cnt = 0
for line in fh:
  if not line.startswith("X-DSPAM-Confidence:") : continue
    val += float(line.split(':')[1].strip())
    cnt = cnt + 1
    #print(line)

print("Average spam confidence: " +str(val/cnt))
