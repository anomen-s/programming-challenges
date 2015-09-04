'''
Have the function ABCheck(str) take the str parameter being passed 
and return the string true if the characters a and b are separated 
by exactly 3 places anywhere in the string at least once 
(ie. "lane borrowed" would result in true because there is exactly three characters between a and b). 
Otherwise return the string false. 
'''

def ABCheck(s): 

  for i in range(len(s)-4):
    if s[i] == 'a' and s[i+4] == 'b':
      return 'true'
    if s[i] == 'b' and s[i+4] == 'a':
      return 'true'
  return 'false'
    
    
# keep this function call here  
# to see how to enter arguments in Python scroll down
print ABCheck(raw_input())           
