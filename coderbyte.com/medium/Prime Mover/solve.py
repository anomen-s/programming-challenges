
'''
 Using the Python language, have the function PrimeMover(num) return the numth prime number. The range will be from 1 to 10^4. For example: if num is 16 the output should be 53 as 53 is the 16th prime number.

'''

def sieve(r):
    primes = range(r)
    primes[0] = False
    primes[1] = False
    # find primes
    for p in xrange(2, len(primes)/2+1):
      if primes[p]:
        i = p + p
        while i < r:
          primes[i] = False
          i = i + p
    return primes


def PrimeMover(n): 
 s = sieve(2*10**4)
 i = 0
 for prime in s:
   if prime:
    i = i + 1
    if i == int(n):
      return prime
 return -1

# keep this function call here  
# to see how to enter arguments in Python scroll down
print PrimeMover(raw_input())  







