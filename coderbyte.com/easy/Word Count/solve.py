'''
Have the function WordCount(str) take the str string parameter being passed 
and return the number of words the string contains 
(ie. "Never eat shredded wheat" would return 4). 
Words will be separated by single spaces. 
'''

def WordCount(str): 

  return len(str.strip().split(' '))

    
    
# keep this function call here  
# to see how to enter arguments in Python scroll down
print WordCount(raw_input())           
