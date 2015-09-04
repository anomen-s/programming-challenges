'''
Have the function SimpleMode(arr) take the array of numbers stored in arr 
and return the number that appears most frequently (the mode). 
For example: if arr contains [10, 4, 5, 2, 4] the output should be 4. 
If there is more than one mode return the one that appeared in the array first 
(ie. [5, 10, 10, 6, 5] should return 5 because it appeared first). 
If there is no mode return -1. The array will not be empty. 
'''

def SimpleMode(arr): 
  occ = {}
  for a in arr:
    if occ.has_key(a):
      occ[a] = occ[a] + 1
    else:
      occ[a] = 1
  counts = occ.values()
  counts.sort()
  maxCount = counts[-1]
  if maxCount < 2:
    return -1
  maxNumbers = []
  for a in occ.keys():
    if occ[a] == maxCount: 
      maxNumbers.append(a)
  for a in arr:
    if maxNumbers.count(a) > 0:
      return a
  return -1

# keep this function call here  
# to see how to enter arguments in Python scroll down
print SimpleMode(raw_input())  
















 