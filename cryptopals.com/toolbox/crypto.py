import itertools
import tools
from Crypto.Cipher import AES

__all__ = [ "xorBytes",
            "encyptCBC", "decyptCBC" ]


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
###               AES CBC crypto with PKCS#7 padding                  ###
#########################################################################

def encryptCBC(key, data):
    data = tools.addPadding(data)
    blocks = tools.split(data, 16, False)

    iv = b'\000' * 16
    result = b''
    
    cipher=AES.new(key, AES.MODE_ECB)
    
    for block in blocks:
      inBlock = xor(block, iv)
      encBlock = cipher.encrypt(inBlock)
      iv = encBlock
      result += encBlock
    
    return result
    
def decryptCBC(key, data):
    encBlocks = tools.split(data, 16, False)

    iv = b'\000' * 16
    result = b''
    
    cipher=AES.new(key, AES.MODE_ECB)
    
    for block in encBlocks:
      decBlock = cipher.decrypt(block)
      dec = xor(decBlock, iv)
      iv = block
      result += dec
    return tools.stripPadding(result)


#########################################################################
###               Tests                                               ###
#########################################################################


if  __name__ == '__main__':
  print("No Tests")

