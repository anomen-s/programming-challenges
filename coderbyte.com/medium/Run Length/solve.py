'''
Have the function RunLength(str) take the str parameter being passed 
and return a compressed version of the string using the Run-length encoding algorithm. 
This algorithm works by taking the occurrence of each repeating character 
and outputting that number along with a single character of the repeating sequence. 

For example: "wwwggopp" would return 3w2g1o2p. 
The string will not contain any numbers, punctuation, or symbols. 
'''

def RunLength(s): 
  res = ''
  lastc = ''
  rl = 0
  for c in s:
     if c == lastc:
         rl = rl + 1
     else:
      if lastc != '':
        res = res + str(rl) + lastc
      rl = 1
      lastc = c
  if lastc != '':
    res = res + str(rl) + lastc
  return res

      
        
    
# keep this function call here  
# to see how to enter arguments in Python scroll down
print RunLength(raw_input())  
















  