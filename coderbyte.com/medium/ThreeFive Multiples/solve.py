'''
Have the function ThreeFiveMultiples(num) return the sum of all the multiples of 3 and 5 that are below num. 

For example: if num is 10, the multiples of 3 and 5 that are below 10 are 3, 5, 6, and 9, 
and adding them up you get 23, so your program should return 23. 

The integer being passed will be between 1 and 100. 
'''

def ThreeFiveMultiples(num): 

  num = int(num)
  s3 = sum(range(3,num, 3))
  s5 = sum(range(5,num, 5))
  s15 = sum(range(15,num, 15))

  return s3 + s5 - s15
    
    
# keep this function call here  
# to see how to enter arguments in Python scroll down
print ThreeFiveMultiples(raw_input())           
