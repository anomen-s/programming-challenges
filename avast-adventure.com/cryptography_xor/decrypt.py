#!/usr/bin/env python3

def guessPass(ciphered, guess):

  l = len(guess)
  pw = [x ^ y for (x,y) in zip(guess,ciphered[0:l])]
  print('password:', bytes(pw))
  dec = bytes([c ^ pw[i % l] for (i, c) in enumerate(ciphered)])
  return dec


with open("flag", "rb") as f:
   c = f.read()

while True:
 print("guess plaintext:")
 guess=bytes(input(),'utf-8')
 dec = guessPass(c, guess);
 print('plaintext:', dec)
