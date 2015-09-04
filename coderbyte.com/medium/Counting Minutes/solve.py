'''
Have the function CountingMinutes(str) take the str parameter being passed 
which will be two times (each properly formatted with a colon and am or pm) 
separated by a hyphen and return the total number of minutes between the two times. 
The time will be in a 12 hour clock format. For example: if str is 9:00am-10:00am 
then the output should be 60. If str is 1:00pm-11:00am the output should be 1320. 
'''
def isDigit(s):
  return s >= '0' and s <= '9'

def decodeNumber(timeArr):
  r = ''
  while isDigit(timeArr[0]):
    r = r + timeArr.pop(0)
  return int(r)

def decodeTime(timeArr):
  h = decodeNumber(timeArr)
  timeArr.pop(0) # :
  m = decodeNumber(timeArr)
  hd = timeArr.pop(0)
  timeArr.pop(0) # m
  time = h*60 + m
  if hd == 'p':
    time = time + 12 * 60
  return time

def CountingMinutes(str): 

  timeArr = list(str)
  t1 = decodeTime(timeArr)
  dash = timeArr.pop(0)
  if dash != '-':
    return -1
  t2 = decodeTime(timeArr)

  if t2 < t1:
    t2 = t2 + 24 * 60
  return t2 - t1


    
# keep this function call here  
# to see how to enter arguments in Python scroll down
print CountingMinutes(raw_input())           
