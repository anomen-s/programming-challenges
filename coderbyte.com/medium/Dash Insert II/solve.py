'''
Using the Python language, have the function DashInsertII(str) insert dashes ('-') between each two odd numbers 
and insert asterisks ('*') between each two even numbers in str. 

For example: if str is 4546793 the output should be 454*67-9-3. 
Don't count zero as an odd or even number. 
'''
def DashInsertII(num): 

  r = ''
  lastOdd = False
  lastEven = False
  for c in str(num):
    if lastOdd and '13579'.count(c) > 0:
      r = r + '-' + c
    elif '13579'.count(c) > 0:
      r = r + c
      lastOdd = True
      lastEven = False
    elif lastEven and '2468'.count(c) > 0:
      r = r + '*' + c
    elif '2468'.count(c) > 0:
      r = r + c
      lastOdd = False
      lastEven = True
    else:
      r = r + c
      lastEven = False
      lastOdd = False
  return r


    
# keep this function call here  
# to see how to enter arguments in Python scroll down
print DashInsertII(raw_input())  
















  