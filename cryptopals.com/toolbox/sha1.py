import struct

import tools

__all__ = [ "hexdigest", "toStr",
            "compute", "buildBlocks", "compute_sha1startblock", "compute_sha1block", "BLOCK_LEN" ]

###################################################################
###    SHA1                                                     ###
###################################################################

def toStr(sha1):
    '''
      Converts 5 32bit registers to 40-char hexstring.
    '''
    return ''.join([("%08x"%x) for x in sha1])

def hexdigest(data):
    return toStr(compute(data))

BLOCK_LEN = int(512/8)

_INT32_MASK = 2**32 - 1

def rol(num, cnt):
    topbits = num >> (32-cnt)
    num <<= cnt
    num |= topbits
    num &= _INT32_MASK

    return num

def compute(data):
    blocks = buildBlocks(0, data)
    
    h = compute_sha1startblock(blocks[0])
    
    for block in blocks[1:]:
      h = compute_sha1block(h, block)
    
    return h
    

def buildBlocks(prefixlen, data):
    '''
      Builds blocks for hashing from given data.
    '''
    ml = (prefixlen + len(data)) * 8
    blocks = tools.split(data, BLOCK_LEN)
    if len(blocks[-1]) == BLOCK_LEN:
      blocks.append(b'')
    blocks[-1] = blocks[-1] + b'\x80'
    
    remSpace = BLOCK_LEN - len(blocks[-1])
    if remSpace < 8:
      blocks[-1] = blocks[-1] + b'\x00' * remSpace
      blocks.append(b'\x00' * (BLOCK_LEN - 8))
      remSpace = 8
    if remSpace > 8:
      blocks[-1] = blocks[-1] + b'\x00' * (remSpace  - 8)
    blocks[-1] = blocks[-1] + struct.pack(">q", ml)
    
    return blocks
    
def compute_sha1startblock(block):
    h0 = 0x67452301
    h1 = 0xEFCDAB89
    h2 = 0x98BADCFE
    h3 = 0x10325476
    h4 = 0xC3D2E1F0
    return compute_sha1block((h0,h1,h2,h3,h4), block)


def compute_sha1block(hx, block):
    h0,h1,h2,h3,h4 = hx
    w = [0] * 80
    w = list(struct.unpack('>16I', block)) + ([0] * 64)

    for i in range(16, 80):
      w[i] = rol(w[i-3] ^ w[i-8] ^ w[i-14] ^ w[i-16], 1)

    a = h0
    b = h1
    c = h2
    d = h3
    e = h4

    for i in range(80):
        if i <= 19:
            f = (b & c) ^ ((~ b) & d)
            k = 0x5A827999
        elif i <= 39:
            f = b ^ c ^ d
            k = 0x6ED9EBA1
        elif i <= 59:
            f = (b & c) ^ (b & d) ^ (c & d) 
            k = 0x8F1BBCDC
        else:
            f = b ^ c ^ d
            k = 0xCA62C1D6

        temp = (rol(a,5) + f + e + k + w[i]) & _INT32_MASK
        e = d
        d = c
        c = rol(b, 30)
        b = a
        a = temp

    h0 = (h0 + a) & _INT32_MASK
    h1 = (h1 + b) & _INT32_MASK
    h2 = (h2 + c) & _INT32_MASK
    h3 = (h3 + d) & _INT32_MASK
    h4 = (h4 + e) & _INT32_MASK

      
    
    return (h0,h1,h2,h3,h4)


##########################################################
###          TESTS                                     ###

def _sha1_tests():
  for i in range(1,3000):
    data = b'X' * i
    exp = _sha1prov(data)
    h = compute(data)
    if exp != toStr(h):
      raise Exception('%i invalid hash: %s , exp: %s' % (i, toStr(h), exp))


def _sha1prov(data):
 import hashlib
 h = hashlib.sha1()
 h.update(data)
 tools.d(['sign data:', data])
 return h.hexdigest()

if __name__ =='__main__':

  _sha1_tests()
  print("Tests finished")


