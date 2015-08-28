'''
Using the Python language, have the function PowersofTwo(num) take the num parameter being passed 
which will be an integer and return the string true if it's a power of two. 
If it's not return the string false. 

For example if the input is 16 then your program should return the string true 
but if the input is 22 then the output should be the string false.

'''

def PowersofTwo(num): 
 p = 2
 while p < num:
   p = p * 2

 return str(num == p).lower()

    
# keep this function call here  
# to see how to enter arguments in Python scroll down
print PowersofTwo(raw_input())  



def isPower2(n):
 p = 2
 while p < n:
   p = p * 2
 
 return (n == p)


print(isPower2(256))
