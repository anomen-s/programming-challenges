'''
Using the Python language, have the function AdditivePersistence(num) take the num parameter being passed 
which will always be a positive integer and return its additive persistence 
which is the number of times you must add the digits in num until you reach a single digit. 
For example: if num is 2718 then your program should return 2 because 2 + 7 + 1 + 8 = 18 and 1 + 8 = 9 and you stop at 9. 
'''

def AdditivePersistence(num): 
   steps = 0
   while num > 9:
     snum = str(num)
     sdigits = list(snum)
     digits = [int(x) for x in sdigits]
     num = sum(digits)
     steps = steps + 1
   return steps

    
    
# keep this function call here  
# to see how to enter arguments in Python scroll down
print AdditivePersistence(raw_input())  
















  