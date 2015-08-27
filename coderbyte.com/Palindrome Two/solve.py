'''
Using the Python language, have the function PalindromeTwo(str) take the str parameter being passed and return the string true if the parameter is a palindrome, (the string is the same forward as it is backward) otherwise return the string false. The parameter entered may have punctuation and symbols but they should not affect whether the string is in fact a palindrome. For example: "Anne, I vote more cars race Rome-to-Vienna" should return true.

'''

def cleanStr(s):
  r = ''
  for c in s.lower():
    rc = ''
    if c >= '0' and c<= '9':
      rc = c
    elif c >= 'a' and c<= 'z':
      rc = c
    r = r + rc
  return r
  
def PalindromeTwo(str): 

  s=cleanStr(str)
  if s == s[::-1]:
    return 'true'
  return 'false'
    
    
# keep this function call here  
# to see how to enter arguments in Python scroll down
print PalindromeTwo(raw_input())  
















  