'''
Using the Python language, have the function MultiplicativePersistence(num) 
take the num parameter being passed which will always be a positive integer 
and return its multiplicative persistence which is the number of times 
you must multiply the digits in num until you reach a single digit. 

For example: if num is 39 then your program should return 3 
because 3 * 9 = 27 then 2 * 7 = 14 and finally 1 * 4 = 4 and you stop at 4. 
'''
def MultiplicativePersistence(num): 
   steps = 0
   while num > 9:
     snum = str(num)
     sdigits = list(snum)
     num = 1
     for snum in sdigits:
        n = int(snum)
        num = num * n
     steps = steps + 1
   return steps

    
# keep this function call here  
# to see how to enter arguments in Python scroll down
print MultiplicativePersistence(raw_input())  

