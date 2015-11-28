import base64
import time

__all__ = [ "d", "setDebug", "start", "end", "run",
            "toHex", "toB64", "fromB64", "fromHex",
            "transpose" ]

#########################################################################
###             DEBUGGING                                             ###
#########################################################################

_DEBUG = False

def setDebug(val=True):
    global _DEBUG
    _DEBUG = val

def d(args):
    if _DEBUG:
      print(args)

_TSTART = 0

def start():
  global _TSTART
  _TSTART = time.time()

def end():
  print(['time[ms]',int((time.time() - _TSTART)*1000)])


def run(main_method, debug=True):
    setDebug(debug)
    start()
    main_method()
    end()
#########################################################################
###             General conversions                                   ###
#########################################################################

def toHex(data, maxLen=0, upperCase=True):
  if (type(data) == str):
    data = bytes(data,'utf-8')
  if maxLen:
    data = data[:maxLen]
  hex=str(base64.b16encode(data),'utf-8')
  if not upperCase:
    hex= hex.lower()
  return hex

def toB64(data, maxLen=0):
  if (type(data) == str):
    data = bytes(data,'utf-8')
  if maxLen:
    data = data[:maxLen]
  b64=base64.b64encode(data)
  return str(b64,'utf-8')

def fromB64(data):
  if (type(data) == str):
    data = bytes(data,'utf-8')
  b64=base64.b64decode(data)
  return b64

def fromHex(s):
    '''
      Convert hex string to bytes
    '''
    if (type(s) == bytes):
      s = str(s, 'utf-8')
    return bytes.fromhex(s)
    

#########################################################################
###             Block operations                                      ###
#########################################################################

def transpose(data, blocklen, skipPartial=True):
  if (type(data) == str):
    data = bytes(data,'utf-8')
  cnt = len(data)//blocklen
  tbl = [bytes([data[n*blocklen+idx] for n in range(cnt)]) for idx in range(blocklen)]


  if not skipPartial:
    lastBlock = data[cnt*blocklen:]
    for (idx, val) in enumerate(lastBlock):
      tbl[idx] += bytes(chr(val),'utf-8')

  return tbl

def detranspose(blocks):
  if len(blocks) == 0:
     return b'' 

  l = len(blocks)
  res = bytearray(len(blocks[0])*l)
  for (idx, bl) in enumerate(blocks):
    for (iidx, item) in enumerate(bl):
      res[iidx*l+idx] = item
#      print(['set',iidx*l+idx,item, res])
  return res


#########################################################################
###             Tests                                                 ###
#########################################################################

def _conv_tests():
   if toB64(b'abcdef') != 'YWJjZGVm' or toB64('abcdef') != 'YWJjZGVm':
     print('base64 encode error')
     exit(1)
   if fromB64(b'YWJjZGVm') != b'abcdef' or fromB64('YWJjZGVm') != b'abcdef':
     print('base64 decode error')
     exit(1)

   if toHex(b'1234') != '31323334' or toHex('1234') != '31323334':
     print('hex encode error')
     exit(1)
   if fromHex(b'31323334') != b'1234' or fromHex('31323334') != b'1234':
     print('hex decode error')
     exit(1)
   
def _transpose_tests():
    blcks = transpose(b'0123456', 3, True)
    if (len(blcks) != 3) or (blcks[0] != b'03') or (blcks[2] != b'25'):
      print('error: ' + str(blcks))
      exit(1)

    decblck = detranspose(blcks)
    if (decblck) != b'012345':
      print('error detranspose: ' + str(decblck))
      exit(1)

    blcks = transpose(b'0123456', 2, False)
    if (len(blcks) != 2) or (blcks[0] != b'0246') or (blcks[1] != b'135'):
      print('error: ' + str(blcks))
      exit(1)

    decblck = detranspose(blcks)
    if (decblck) != b'0123456\000':
      print('error detranspose: ' + str(decblck))
      exit(1)
    

if  __name__ == '__main__':
  _transpose_tests()
  _conv_tests()
  print("Tests Passed")

