'''
Using the Python language, have the function CheckNums(num1,num2) take both parameters being passed 
and return the string true if num2 is greater than num1, 
otherwise return the string false. 

If the parameter values are equal to each other then return the string -1. 
'''

def CheckNums(num1,num2): 

  if num1 == num2:
     return '-1'
  n1 = int(num1)
  n2 = int(num2)
  
  if n2 > n1:
    return 'true'
  return 'false'
    
# keep this function call here  
# to see how to enter arguments in Python scroll down
print CheckNums(raw_input())  



