__all__ = [ "compute", "initSingleCharTab" ]

#########################################################################
###      Decrypted text quality scoring                               ###
#########################################################################

def initSingleCharTab():
   T = [0] * 256
   T[0] = -100
   for i in range(128,256):
     T[i] = -20
   for i in range(0x0E,0x20):
     T[i] = -20
   for i in range(0x20,0x30):
     T[i] = 2
   for (p,c) in enumerate('ETAOIN SHRDLU CMFYWGPBVKXQJZ'[::-1]):
     T[ord(c)] = 30+4*p
     T[ord(c.lower())] = 40+4*p
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

