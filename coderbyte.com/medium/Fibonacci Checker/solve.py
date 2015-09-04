'''
Have the function FibonacciChecker(num) return the string yes if the number given is part of the Fibonacci sequence. 
This sequence is defined by: Fn = Fn-1 + Fn-2, which means to find Fn you add the previous two numbers up. 
The first two numbers are 0 and 1, then comes 1, 2, 3, 5 etc. 
If num is not in the Fibonacci sequence, return the string no.
'''

def fib():
  f1 = 0
  f2 = 1 
  yield f1
  yield f2
  while True:
    f1, f2 = f2, (f1 + f2)
    yield f2
  
def FibonacciChecker(num): 

  num = int(num)
  for f in fib():
    if f > num:
      return 'no'
    if f == num:
      return 'yes'
    
  return 'no'
    
    
# keep this function call here  
# to see how to enter arguments in Python scroll down
print FibonacciChecker(raw_input())           

