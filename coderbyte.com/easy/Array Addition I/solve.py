'''
Using the Python language, have the function ArrayAdditionI(arr) take the array of numbers stored in arr 
and return the string true if any combination of numbers in the array can be added up to equal the largest number in the array, 
otherwise return the string false. 

For example: if arr contains [4, 6, 23, 10, 1, 3] the output should return true because 4 + 6 + 10 + 3 = 23. 

The array will not be empty, will not contain all the same elements, and may contain negative numbers. 
'''

def countFor(arr, m, s0):
  if len(arr) == 0:
    return False
  a0 = arr[0]
  ar = arr[1:]
  
  sw = s0 + a0
  if sw == m:
    return True
  if countFor(ar, m, sw):
    return True
  if countFor(ar, m, s0):
    return True
  return False
  
def ArrayAdditionI(arr): 
 
  m = max(arr)
  arr.remove(m)
  return str(countFor(arr, m, 0)).lower()

    
# keep this function call here  
# to see how to enter arguments in Python scroll down
print ArrayAdditionI(raw_input())  
















  