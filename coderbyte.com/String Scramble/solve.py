'''
Using the Python language, have the function StringScramble(str1,str2) take both parameters 
being passed and return the string true if a portion of str1 characters can be rearranged to match str2, 
otherwise return the string false. 

For example: if str1 is "rkqodlw" and str2 is "world" the output should return true. 
Punctuation and symbols will not be entered with the parameters. 
'''

def charCounts(s):
    clist = {}
    for c in s:
      if c in clist:
        clist[c] = clist[c] + 1
      else:
        clist[c] = 1
    return clist

def cSubset(cl1, cl2):
     for c in cl2.keys():
       if not c in cl1:
          return False
       if cl1[c] < cl2[c]:
          return False
     return True

def StringScramble(str1,str2): 
  cl1 = charCounts(str1)
  cl2 = charCounts(str2)
  
  return  str(cSubset(cl1, cl2)).lower()
    
    
# keep this function call here  
# to see how to enter arguments in Python scroll down
print StringScramble(raw_input())  
















  