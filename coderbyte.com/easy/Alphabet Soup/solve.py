'''
Have the function AlphabetSoup(str) take the str string parameter being passed 
and return the string with the letters in alphabetical order (ie. hello becomes ehllo). 
Assume numbers and punctuation symbols will not be included in the string. 
'''
def AlphabetSoup(str): 

  l = list(str)
  l.sort()
  return ''.join(l)
    
    
# keep this function call here  
# to see how to enter arguments in Python scroll down
print AlphabetSoup(raw_input())           
