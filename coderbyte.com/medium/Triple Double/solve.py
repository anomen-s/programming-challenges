def TripleDouble(num1,num2): 
  snum1 = str(num1)
  snum2 = str(num2)
  for n in range(10):
    triple = str(n)*3
    double = str(n)*2
    if snum1.find(triple) >= 0:
      if snum2.find(double) >= 0:
        return 1

  return 0
    

#print TripleDouble(451999277, 41177722899)  
    
# keep this function call here  
# to see how to enter arguments in Python scroll down
print TripleDouble(raw_input())  
















  