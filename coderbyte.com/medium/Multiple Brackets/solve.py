'''
Have the function MultipleBrackets(str) take the str parameter being passed 
and return 1 #ofBrackets if the brackets are correctly matched 
and each one is accounted for. Otherwise return 0. 
For example: if str is "(hello [world])(!)", then the output should be 1 3 
because all the brackets are matched and there are 3 pairs of brackets, 
but if str is "((hello [world])" the the output should be 0 
because the brackets do not correctly match up. 
Only "(", ")", "[", and "]" will be used as brackets. 
If str contains no brackets return 1. 
'''
def brackets(s): 

  brackets = []
  count = 0
  for c in s:
    if (c == '(') :
      brackets.append(')')
      count = count + 1
    if (c == '['):
      brackets.append(']')
      count = count + 1
    if (c == ')') or (c == ']'):
      if len(brackets) == 0:
        return [0]
      cb = brackets.pop()
      if cb != c:
        return [0]
  if len(brackets) > 0:
    return [0]
  if count == 0:
    return [1]
  return [1, count]        
  
def MultipleBrackets(s): 
  b = brackets(s)
  return ' '.join([str(x) for x in b])
    
# keep this function call here  
# to see how to enter arguments in Python scroll down
print MultipleBrackets(raw_input())  
















  