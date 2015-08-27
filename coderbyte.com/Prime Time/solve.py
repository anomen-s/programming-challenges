'''
Have the function PrimeTime(num) take the num parameter being passed 
and return the string true if the parameter is a prime number, 
otherwise return the string false. 

The range will be between 1 and 2^16. 
'''
import math

def isPrime(N):
  i = 2
  while i <= math.sqrt(N):
    if (N % i) == 0:
      return False
    i = i + 1
  return True


def PrimeTime(num):

  if isPrime(int(num)):
    return 'true'
  return 'false'

    
# keep this function call here  
# to see how to enter arguments in Python scroll down
print PrimeTime(raw_input())  

