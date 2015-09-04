'''
Have the function DistinctList(arr) take the array of numbers stored in arr 
and determine the total number of duplicate entries. 

For example if the input is [1, 2, 2, 2, 3] 
then your program should output 2 because there are two duplicates of one of the elements. 
'''

def DistinctList(arr): 
  found = set()
  dupes = 0
  for num in arr:
    if num in found:
      dupes = dupes+1
    else:
      found.add(num)

  return dupes
    
    
# keep this function call here  
# to see how to enter arguments in Python scroll down
print DistinctList(raw_input())           

