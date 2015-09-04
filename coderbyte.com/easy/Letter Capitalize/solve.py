'''
Have the function LetterCapitalize(str) take the str parameter being passed 
and capitalize the first letter of each word. 
Words will be separated by only one space. 
'''
def LetterCapitalize(str): 

  f = True
  r = ''
  for c in str:
    if c >= 'a' and c <= 'z' and f:
       c = c.upper()
    f = (c == ' ')
    r = r + c
  return r
    
    
    
# keep this function call here  
# to see how to enter arguments in Python scroll down
print LetterCapitalize(raw_input())           
