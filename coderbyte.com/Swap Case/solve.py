'''
Have the function SwapCase(str) take the str parameter and swap the case of each character. 
For example: if str is "Hello World" the output should be hELLO wORLD. 
Let numbers and symbols stay the way they are. 
'''

def isLower(c):
   return (c >= 'a' and c <= 'z')

def isUpper(c):
   return (c >= 'A' and c <= 'Z')

def SwapCase(s):
     r = ''
     for c in s:
       if isLower(c):
         r = r + c.upper()
       elif isUpper(c):
         r = r + c.lower()
       else:
         r = r + c
     return r

#print swapCase('abcDEF')
    
# keep this function call here  
# to see how to enter arguments in Python scroll down
print SwapCase(raw_input())           
    


   