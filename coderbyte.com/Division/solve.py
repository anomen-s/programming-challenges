'''
Using the Python language, have the function Division(num1,num2) take both parameters 
being passed and return the Greatest Common Factor. 

That is, return the greatest number that evenly goes into both numbers with no remainder. 
For example: 12 and 16 both are divisible by 1, 2, and 4 so the output should be 4. 
The range for both parameters will be from 1 to 10^3. 

https://en.wikipedia.org/wiki/Euclidean_algorithm
'''

def gcd(u, w):

  while w > 0:
    u, w = w, (u % w)
  return u


def Division(num1,num2): 
  return gcd(int(num1), int(num2))
    
    
# keep this function call here  
# to see how to enter arguments in Python scroll down
print Division(raw_input())  

  
 
#print gcd(12, 16) # 4
#print gcd(40902, 24140)  # 34
#print gcd( 24140, 40902)
