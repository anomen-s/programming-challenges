'''
Have the function DashInsert(str) insert dashes ('-') between each two odd numbers in str. 
For example: if str is 454793 the output should be 4547-9-3. 
Don't count zero as an odd number. 
'''

def DashInsert(s): 

  r = ''
  lastOdd = False
  for c in str(s):
    if lastOdd and '13579'.count(c) > 0:
      r = r + '-' + c
    elif '13579'.count(c) > 0:
      r = r + c
      lastOdd = True
    else:
      r = r + c
      lastOdd = False
  return r
    
    
# keep this function call here  
# to see how to enter arguments in Python scroll down
print DashInsert(raw_input())     