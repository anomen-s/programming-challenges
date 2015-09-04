'''
Have the function LongestWord(sen) take the sen parameter being passed and return the largest word in the string. 
If there are two or more words that are the same length, return the first word from the string with that length. 
Ignore punctuation and assume sen will not be empty.

'''

def LongestWord(sen): 

  s1 = [punct(c) for c in sen]
  s2 = ''.join(s1)
  words = s2.split(' ')
  lw = ''
  for w in words :
    if len(w) > len(lw):
      lw = w
  return lw
    
    
def punct(c):
  cl = c.lower()
  if cl <= '9' and cl >= '0':
      return c
  if cl <= 'z' and cl >= 'a':
      return c
  return ' '


# keep this function call here  
# to see how to enter arguments in Python scroll down
print LongestWord(raw_input())     
