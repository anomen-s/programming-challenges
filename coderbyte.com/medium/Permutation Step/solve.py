'''
Using the Python language, have the function PermutationStep(num) take the num parameter being passed 
and return the next number greater than num using the same digits. 

For example: if num is 123 return 132, if it's 12453 return 12534. 
If a number has no greater permutations, return -1 (ie. 999). 
'''
def toNum(arr):
  sArr = [str(x) for x in arr]
  return int(''.join(sArr))

def PermutationStep(num): 

  res = -1
  digits = list(str(num))

  # try to reorder smallest possible set first
  for fixcount in range(len(digits)-1,-1,-1):
    fixed = digits[:fixcount]
    var = digits[fixcount:]
    for n in var:
      # reorder variable part
      if n > var[0]:
        vartmp = var[:]
        vartmp.remove(n)
        vartmp.sort()
        vartmp.insert(0, n)
        numRes = toNum(fixed + vartmp)
        if (numRes > num) and ((res == -1) or (numRes < res)):
          res = numRes
    # todo: return here if result found (it cannot be better)
  return res
        
    
# keep this function call here  
# to see how to enter arguments in Python scroll down
print PermutationStep(raw_input())  
















  