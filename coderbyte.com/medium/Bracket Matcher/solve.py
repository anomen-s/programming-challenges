'''
Using the Python language, have the function BracketMatcher(str) take the str parameter being passed 
and return 1 if the brackets are correctly matched and each one is accounted for. 
Otherwise return 0. 
For example: if str is "(hello (world))", then the output should be 1, 
but if str is "((hello (world))" the the output should be 0 
because the brackets do not correctly match up. 
Only "(" and ")" will be used as brackets. If str contains no brackets return 1.

'''
def BracketMatcher(s): 

  brackets = 0
  for c in s:
    if (c == '(') :
      brackets = brackets + 1
    if (c == ')'):
      if brackets <= 0:
        return 0
      brackets = brackets - 1
  if brackets > 0:
    return 0
  return 1

    
# keep this function call here  
# to see how to enter arguments in Python scroll down
print BracketMatcher(raw_input())  
















  