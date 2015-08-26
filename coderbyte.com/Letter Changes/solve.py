'''

Have the function LetterChanges(str) take the str parameter being passed and modify it using the following algorithm. 
Replace every letter in the string with the letter following it in the alphabet (ie. c becomes d, z becomes a). 
Then capitalize every vowel in this new string (a, e, i, o, u) and finally return this modified string.

'''

def LetterChanges(s): 
  result = ''
  for i in range(len(s)):
    c = s[i]
    if c >='a' and c < 'z':
      c = chr(ord(c)+1)
    elif c == 'z':
      c = 'a'
    if c >='A' and c < 'Z':
      c = chr(ord(c)+1)
    elif c == 'Z':
      c = 'a'
    if 'aeiou'.count(c) > 0:
       c = c.upper()
    
    result = result + c
  return result
    
    
# keep this function call here  
# to see how to enter arguments in Python scroll down
print LetterChanges(raw_input())           
