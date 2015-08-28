'''
Using the Python language, have the function TimeConvert(num) take the num parameter being passed and return the number of hours and minutes the parameter converts to (ie. if num = 63 then the output should be 1:3). Separate the number of hours and minutes with a colon.
'''

def TimeConvert(num): 

  h = int(num) // 60
  m = int(num) % 60
  return '%i:%i' % (h,m) 
    
    
# keep this function call here  
# to see how to enter arguments in Python scroll down
print TimeConvert(raw_input())  
















   