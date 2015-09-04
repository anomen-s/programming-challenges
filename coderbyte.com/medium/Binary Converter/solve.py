'''
Using the Python language, have the function BinaryConverter(str) return the decimal form of the binary value. 
For example: if 101 is passed return 5, or if 1000 is passed return 8.

'''

def BinaryConverter(s): 

  r = 0
  v = 1
  for i in s[::-1]:
    if i == '1':
      r = r + v
    v = v * 2
  return r
    
# keep this function call here  
# to see how to enter arguments in Python scroll down
print BinaryConverter(raw_input())  





