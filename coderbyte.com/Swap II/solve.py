'''
Using the Python language, have the function SwapII(str) take the str parameter 
and swap the case of each character. Then, if a letter is between two numbers 
(without separation), switch the places of the two numbers. 
For example: if str is "6Hello4 -8World, 7 yes3" 
the output should be 4hELLO6 -8wORLD, 7 YES3. 
'''
def isDigit(c):
  return c >= '0' and c <= '9'

def isLetter(c):
  return (c.lower() >= 'a') and (c.lower() <= 'z')

def swapCase(c):
  if c == c.upper():
    return c.lower()
  else:
    return c.upper()
  
def SwapII(s): 
  sswap = [swapCase(x) for x in s]

  digitPos = None
  letters = None
  for i in range(len(sswap)):
    c = sswap[i]
    if isDigit(c):
      if letters and (digitPos != None):
          sswap[i] = sswap[digitPos] 
          sswap[digitPos]  = c
      letters = None
      digitPos = i
    elif isLetter(c):
        if letters == None:
          letters = True
    else:
        letters = False
  return ''.join(sswap) 
    
    
# keep this function call here  
# to see how to enter arguments in Python scroll down
print SwapII(raw_input())  
















  