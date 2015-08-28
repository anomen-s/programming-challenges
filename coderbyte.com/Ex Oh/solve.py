'''
Using the Python language, have the function ExOh(str) take the str parameter being passed 
and return the string true if there is an equal number of x's and o's, 
otherwise return the string false. 
Only these two letters will be entered in the string, no punctuation or numbers. 
For example: if str is "xooxxxxooxo" then the output should return false because there are 6 x's and 5 o's. 
'''

def ExOh(s): 

  ohs = 0
  exs = 0
  for c in s:
    if c == 'o':
      ohs = ohs + 1
    elif c == 'x':
      exs = exs + 1
  return str(ohs == exs).lower()
    
    
# keep this function call here  
# to see how to enter arguments in Python scroll down
print ExOh(raw_input())  
















  