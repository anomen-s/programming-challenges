'''
Have the function LetterCountI(str) take the str parameter being passed 
and return the first word with the greatest number of repeated letters. 

For example: "Today, is the greatest day ever!" 
should return greatest because it has 2 e's (and 2 t's) and it comes before ever 
which also has 2 e's. 

If there are no words with repeating letters return -1. 
Words will be separated by spaces. 
'''
def LetterCountI(s): 
  words = s.split(' ')
  mwc = 0
  mw = ''
  for word in words:
    wc = countChars(word)
    if wc > mwc:
      mwc = wc
      mw = word
  if mwc < 2:
    return '-1'
  return mw

def countChars(s):
    clist = {}
    for c in s:                    
      if c in clist:               
        clist[c] = clist[c] + 1    
      else:                        
        clist[c] = 1               
    return max(clist.values())
  
    
# keep this function call here  
# to see how to enter arguments in Python scroll down
print LetterCountI(raw_input())           
