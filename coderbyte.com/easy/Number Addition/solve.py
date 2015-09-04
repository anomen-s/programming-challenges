'''
Have the function NumberSearch(str) take the str parameter, 
search for all the numbers in the string, add them together, 
then return that final number. 
For example: if str is "88Hello 3World!" the output should be 91. 
You will have to differentiate between single digit numbers and multiple digit numbers like in the example above. 
So "55Hello" and "5Hello 5" should return two different answers. 
Each string will contain at least one letter or symbol. 
'''

def isDigit(s):
  return s >= '0' and s <= '9'

def decodeNumber(timeArr):
  r = ''
  while len(timeArr) > 0 and isDigit(timeArr[0]):
    r = r + timeArr.pop(0)
  return r


def NumberAddition(s):
  arr = list(s)
  nums = []
  while len(arr) > 0:
    print arr
    num = decodeNumber(arr)
    while len(arr) > 0 and not isDigit(arr[0]):
      arr.pop(0)
    if len(num) > 0:
      nums.append(int(num))
  return sum(nums)

#print(NumberAddition('94fdfs4'))

# keep this function call here  
# to see how to enter arguments in Python scroll down
print NumberAddition(raw_input())           
