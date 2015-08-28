def numformat(s):
  nr = s[::-1]
  c = 0
  r = ''
  sep = ''
  for i in nr:
    r = r + sep
    sep = ''
    r = r + i
    if c % 3 == 2:
      sep = ','
    c = c + 1
  return r[::-1]
  
def DivisionStringified(num1,num2): 

  val = float(num1) / float(num2)
  val = int(round(val)) 
  return numformat(str(val))
    
    
# keep this function call here  
# to see how to enter arguments in Python scroll down
print DivisionStringified(raw_input())           
