'''
Using the Python language, have the function NoughtsDeterminer(strArr) take the strArr parameter 
being passed which will be an array of size eleven. 
The array will take the shape of a Tic-tac-toe board with spaces strArr[3] and strArr[7] 
being the separators ("<>") between the rows, 
and the rest of the spaces will be either "X", "O", or "-" which signifies an empty space. 
So for example strArr may be ["X","O","-","<>","-","O","-","<>","O","X","-"]. 
This is a Tic-tac-toe board with each row separated double arrows ("<>"). 
Your program should output the space in the array by which any player could win 
by putting down either an "X" or "O". 
In the array above, the output should be 2 because if an "O" is placed in strArr[2] 
then one of the players wins. 
Each board will only have one solution for a win, not multiple wins. 
You output should never be 3 or 7 because those are the separator spaces. 
'''

LINES = [
(0,0,1,0),(0,0,0,1),(0,0,1,1),
(1,0,0,1),
(2,0,0,1),(2,0,-1,1),
(0,1,1,0),
(0,2,1,0),
]
def getWinningPos(board):
  for (x,y,dx,dy) in LINES:
     if isWinningPos(board, x,y,dx,dy):
        return (x,y,dx,dy)
  return None
 
  
def isWinningPos(board, x, y, dx, dy):
  c1 = board[y][x]
  if c1 == '-':
    return False
  return (c1 == board[y+dy][x+dx] == board[y+2*dy][x+2*dx])
  
  
def makeBoard(arr):
  rows = []
  row = []
  for el in arr:
    if el == "<>":
      rows.append(row)
      row = []
    else:
      row.append(el)
  rows.append(row)
  return rows

def pos(x,y):
  return y * 4 + x

def NoughtsDeterminer(strArr): 
  board = makeBoard(strArr)
  
  for y in range(3):
    for x in range(3):
      if board[y][x] == '-':
        board[y][x] = 'O'
        if getWinningPos(board):
          return pos(x,y)
        board[y][x] = 'X'
        if getWinningPos(board):
          return pos(x,y)
        board[y][x] = '-'
  return -1
    

print NoughtsDeterminer(("X","O","-","<>","-","O","-","<>","O","X","-"))
# keep this function call here  
# to see how to enter arguments in Python scroll down
print NoughtsDeterminer(raw_input())  
















  