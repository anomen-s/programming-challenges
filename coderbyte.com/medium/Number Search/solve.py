'''
Using the Python language, have the function NumberSearch(str) take the str parameter, 
search for all the numbers in the string, add them together, 
then return that final number divided by the total amount of letters in the string. 
For example: if str is "Hello6 9World 2, Nic8e D7ay!" the output should be 2. 
First if you add up all the numbers, 6 + 9 + 2 + 8 + 7 you get 32. 
Then there are 17 letters in the string. 32 / 17 = 1.882, 
and the final answer should be rounded to the nearest whole number, 
so the answer is 2. 
Only single digit numbers separated by spaces will be used throughout the whole string 
(So this won't ever be the case: hello44444 world). 
Each string will also have at least one letter. 
'''

def NumberSearch(s): 

  letters = 0
  digits = 0
  for c in s:
    if c >= 'A' and c <= 'Z':
      letters = letters + 1
    if c >= 'a' and c <= 'z':
      letters = letters + 1
    if c >= '0' and c <= '9':
      digits = digits + int(c)

  return int(round(float(digits) / letters))
        

#print NumberSearch( "H3ello9-9")    
# keep this function call here  
# to see how to enter arguments in Python scroll down
print NumberSearch(raw_input())  
