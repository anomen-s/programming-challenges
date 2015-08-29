'''
Using the Python language, have the function OffLineMinimum(strArr) take the strArr parameter 
being passed which will be an array of integers ranging from 1...n and the letter "E" 
and return the correct subset based on the following rules. 
The input will be in the following format: ["I","I","E","I",...,"E",...,"I"] 
where the I's stand for integers and the E means take out the smallest integer currently in the whole set. 
When finished, your program should return that new set with integers separated by commas. 

For example: if strArr is ["5","4","6","E","1","7","E","E","3","2"] 
then your program should return 4,1,5.
'''

def OffLineMinimum(strArr): 
  
  items = []
  res = []
  for snum in strArr:
    if snum == 'E':
      items.sort()
      res.append(items.pop(0))
    else:
      items.append(int(snum))
  strRes = [str(x) for x in res]
  return ','.join(strRes)
    
 
    
# keep this function call here  
# to see how to enter arguments in Python scroll down
print OffLineMinimum(raw_input())  











  