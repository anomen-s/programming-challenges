
'''
Using the Python language, have the function CoinDeterminer(num) take the input, 
which will be an integer ranging from 1 to 250, 
and return an integer output that will specify the least number of coins, 
that when added, equal the input integer. 
Coins are based on a system as follows: 
there are coins representing the integers 1, 5, 7, 9, and 11. 

So for example: if num is 16, then the output should be 2 
because you can achieve the number 16 with the coins 9 and 7. 
If num is 25, then the output should be 3 
because you can achieve 25 with either 11, 9, and 5 coins or with 9, 9, and 7 coins. 
'''

# todo: store results to speedup

def coinsSelect(num, coins): 
  if len(coins) == 0:
    if num == 0:
      return 0
    else:
      return None
  rem = num
  minCount = num
  c0 = coins[0]
  cRem = coins[1:]
  ccount = rem // c0
  for c in range(0, ccount+1):
      remCount = coinsSelect(num - c * c0, cRem)
      if (remCount != None) and minCount > (remCount + c):
        minCount = remCount + c
  return minCount
  

def CoinDeterminer(num): 
  coins = [1, 5, 7, 9, 11][::-1]
  return coinsSelect(int(num), coins)

print CoinDeterminer(227)  

# keep this function call here  
# to see how to enter arguments in Python scroll down
print CoinDeterminer(raw_input())  
















  