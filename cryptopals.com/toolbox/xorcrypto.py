import  itertools

__all__ = [ "xorBytes" ]


#########################################################################
###               XOR encoding                                        ###
#########################################################################

def xor(s1, key):
    '''
      XOR bytes sequence with password.
    '''
    if (type(key) == int):
      key = [key]
    nums = [(c1 ^ c2) for (c1, c2) in zip(s1, itertools.cycle(key))]
    asBytes = bytes(nums)
    return asBytes

#########################################################################
###               Tests                                               ###
#########################################################################


if  __name__ == '__main__':
  print("No Tests")

