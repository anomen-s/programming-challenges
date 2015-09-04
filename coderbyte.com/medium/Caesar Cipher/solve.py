'''
Have the function CaesarCipher(str,num) take the str parameter and perform a Caesar Cipher shift on it 
using the num parameter as the shifting number. 
A Caesar Cipher works by shifting each letter in the string N places down in the alphabet 
(in this case N will be num). 
Punctuation, spaces, and capitalization should remain intact. 

For example if the string is "Caesar Cipher" and num is 2 the output should be "Ecguct Ekrjgt". 
'''

def CaesarCipher(str,num): 
 
  r = ''
  for c in str:
    if c >= 'a' and c <= 'z':
      c = chr(((ord(c)-ord('a')+num) % 26) + ord('a'))
    if c >= 'A' and c <= 'Z':
      c = chr(((ord(c)-ord('A')+num) % 26) + ord('A'))
    r = r + c
  return r
    
    
# keep this function call here  
# to see how to enter arguments in Python scroll down
print CaesarCipher(raw_input())           
