
__all__ = [ "compute" ]

#########################################################################
###             Hamming distance                                      ###
#########################################################################

def _buildbitdifftable():
    T = [0] * 256
    for idx in range(len(T)):
      T[idx] = (idx & 1) + T[idx >> 1]
    return T

_BDT = _buildbitdifftable()


def compute(str1,str2):
    return sum([_BDT[v1 ^ v2] for (v1, v2) in zip(str1, str2)])


def computeRange(data, lengths):
   print("IMPLEMENT")

#########################################################################
###             Tests                                                 ###
#########################################################################

def hamming_test():
    A=b'this is a test'
    B=b'wokka wokka!!!'
    
    r = compute(A,B)
    print(['result',r])
    if r != 37:
      print('Error in hamming.compute()')
      exit(1)

if  __name__ =='__main__':
  hamming_test()

