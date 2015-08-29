'''
Using the Python language, have the function MeanMode(arr) take the array of numbers stored in arr 
and return 1 if the mode equals the mean, 0 if they don't equal each other 
(ie. [5, 3, 3, 3, 1] should return 1 because the mode (3) equals the mean (3)). 
The array will not be empty, will only contain positive integers, 
and will not contain more than one mode. 
'''

def getMode(arr):
  occ = {}
  for a in arr:
    if occ.has_key(a):
      occ[a] = occ[a] + 1
    else:
      occ[a] = 1
  counts = occ.values()
  counts.sort()
  maxCount = counts[-1]
  if maxCount == 1:
    return None
  for a in occ.keys():
    if occ[a] == maxCount:
      return a
  return None

def MeanMode(arr):
  mode = getMode(arr)
  mean = sum(arr) / len(arr)
  if mode == mean:
    return 1
  return 0
    
    
# keep this function call here  
# to see how to enter arguments in Python scroll down
print MeanMode(raw_input())  
















  