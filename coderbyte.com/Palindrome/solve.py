'''
Using the Python language, have the function Palindrome(str) take the str parameter being passed 
and return the string true if the parameter is a palindrome, 
(the string is the same forward as it is backward) otherwise return the string false. 

For example: "racecar" is also "racecar" backwards. 
Punctuation and numbers will not be part of the string. 
'''

def cleanStr(s):
  r = ''
  for c in s:
    rc = ''
    if c >= '0' and c<= '9':
      rc = c
    elif c >= 'a' and c<= 'z':
      rc = c
    r = r + rc
  return r
  
def Palindrome(str): 

  s=cleanStr(str)
  if s == s[::-1]:
    return 'true'
  return 'false'
    
    
# keep this function call here  
# to see how to enter arguments in Python scroll down
print PalindromeTwo(raw_input())  
















  