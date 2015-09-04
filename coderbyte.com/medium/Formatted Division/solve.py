'''
Using the Python language, have the function FormattedDivision(num1,num2) take both parameters being passed, 
divide num1 by num2, and return the result as a string with properly formatted commas 
and 4 significant digits after the decimal place. 
For example: if num1 is 123456789 and num2 is 10000 the output should be "12,345.6789". 
The output must contain a number in the one's place even if it is a zero. 
'''

def formatFloat(num):
  if num < 0:
    return '-' + formatFloat(-num)
  res = ''
  intPart = int(num)
  decPart = num - intPart
  # int part
  comma = '.'
  commas = 0
  if intPart == 0:
    res = '0.'
  while intPart > 0:
    digit = intPart % 10
    intPart = intPart // 10
    if commas % 3 == 0:
      res = comma + res
      comma = ','
    commas = commas + 1
    res = str(digit) + res
  # decimal part
  for i in range(4):
    decPart = decPart * 10
    if i == 3:
      digit = int(round(decPart))
    else:
      digit = int(decPart)
    decPart = decPart - digit
    res = res + str(digit)
  return res
  
def FormattedDivision(num1,num2): 
  res = float(num1) / float(num2)
  
  return formatFloat(res) 
    
print FormattedDivision(5,54)  
print FormattedDivision(175,24)  
    
# keep this function call here  
# to see how to enter arguments in Python scroll down
print FormattedDivision(raw_input())  
















  