'''
Have the function ArithGeoII(arr) take the array of numbers stored in arr 
and return the string "Arithmetic" if the sequence follows an arithmetic pattern 
or return "Geometric" if it follows a geometric pattern. 
If the sequence doesn't follow either pattern return -1. 
An arithmetic sequence is one where the difference between each of the numbers is consistent, 
where as in a geometric sequence,
each term after the first is multiplied by some constant or common ratio. 
Arithmetic example: [2, 4, 6, 8] and Geometric example: [2, 6, 18, 54]. 
Negative numbers may be entered as parameters, 0 will not be entered, 
and no array will contain all the same elements. 
'''

def isArithmetic(arr):
  diff = arr[1] - arr[0]
  prev = arr[0] - diff
  for n in arr:
    if (n-prev)  != diff:
      return False
    prev = n
  return True

def isGeom(arr):
  coef = 1.0 * arr[1] / arr[0]
  prev = arr[0] / coef
  for n in arr:
    if (prev * coef)  != n:
      return False
    prev = n
  return True

def ArithGeoII(arr): 

  if isArithmetic(arr):
    return  'Arithmetic'
  if isGeom(arr):
    return  'Geometric'
  return '-1'

# keep this function call here  
# to see how to enter arguments in Python scroll down
print ArithGeoII(raw_input())           















