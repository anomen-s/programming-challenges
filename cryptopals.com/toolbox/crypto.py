import itertools
import tools
from Crypto.Cipher import AES
from Crypto import Random

__all__ = [ "genKey",
            "xorBytes",
            "encryptECB", "decryptECB",
            "encryptCBC", "decryptCBC",
            "encryptCTR" ]

#########################################################################
###               Key generation                                      ###
#########################################################################

def genKey(length=16):
 return Random.new().read(length)

#########################################################################
###               XOR encoding                                        ###
#########################################################################

def xor(s1, key):
    '''
      XOR bytes sequence "s1" with password "key" (repeated if necessary).
    '''
    if (type(key) == int):
      key = [key]
    nums = [(c1 ^ c2) for (c1, c2) in zip(s1, itertools.cycle(key))]
    asBytes = bytes(nums)
    return asBytes

#########################################################################
###               AES ECB crypto with PKCS#7 padding                  ###
#########################################################################

def encryptECB(key, data):
    inBlock = tools.addPadding(data)
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.encrypt(inBlock)

def decryptECB(key, data):
    cipher = AES.new(key, AES.MODE_ECB)
    dec = cipher.decrypt(data)
    return tools.stripPadding(dec)

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
###               AES CTR crypto                                      ###
#########################################################################

def encryptCTR(key, nonce, data, littleEndian=False):
    '''
       Perform CTR encrpytion
       Cipher input is 128bit key, 64bit nonce.
       Counter is generated big endian (usual) or little endian.
    '''
    inBlocks = tools.split(data, 16)

    iv = bytearray(nonce + (b'\000' * 8))
    result = b''
    
    cipher=AES.new(key, AES.MODE_ECB)
    
    for inBlock in inBlocks:
      encBlock = cipher.encrypt(bytes(iv))
      enc = xor(inBlock, encBlock)
      _nextBlock(iv, littleEndian)
      result += enc
    return result


def _nextBlock(iv, littleEndian):
    if littleEndian:
      start = 8
      d = 1
      end = 16
    else:
      start = 15
      d = -1
      end = 7
    carry = 1
    for idx in range(start,end,d):
      n = iv[idx] + carry
      iv[idx] = n & 0xFF
      carry = n>>8
      if not carry:
        break

    return iv
#########################################################################
###               Tests                                               ###
#########################################################################


if  __name__ == '__main__':
  print("No Tests")

