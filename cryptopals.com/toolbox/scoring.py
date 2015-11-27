__all__ = [ "compute", "initSingleCharTab" ]

#########################################################################
###      Decrypted text quality scoring                               ###
#########################################################################

def initSingleCharTab():
   T = [0] * 256
   for (p,c) in enumerate('ETAOIN SHRDLU CMFYWGPBVKXQJZ'[::-1]):
     T[ord(c)] = p
     T[ord(c.lower())] = p
   return T
  

_SINGLE_CHAR_T = initSingleCharTab()

def compute(s):
    return sum([_SINGLE_CHAR_T[c] for c in s])


#########################################################################
###             Tests                                                 ###
#########################################################################

def scoring_test(s):
    return 0

if  __name__ =='__main__':
  scoring_test()
  print("Tests Passed")

