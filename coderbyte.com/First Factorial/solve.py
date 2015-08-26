'''
Have the function FirstFactorial(num) take the num parameter being passed and return the factorial of it 
(ie. if num = 4, return (4 * 3 * 2 * 1)). For the test cases, the range will be between 1 and 18.

Use the Parameter Testing feature in the box below to test your code with different arguments. 
'''

def FirstFactorial(num): 

  r = int(num)
  for i in range(1,r):
    r = r * i
  return r
    
    
# keep this function call here  
# to see how to enter arguments in Python scroll down
print FirstFactorial(raw_input())           
