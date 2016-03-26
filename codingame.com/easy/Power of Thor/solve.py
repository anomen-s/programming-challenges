import sys
import math

'''

  The Goal
Your program must allow Thor to reach the light of power.
  Rules
Thor moves on a map which is 40 wide by 18 high. Note that the coordinates (X and Y) start at the top left! 
This means the most top left cell has the coordinates "X=0,Y=0" and the most bottom right one has the coordinates "X=39,Y=17".

Once the program starts you are given:

    the variable lightX: the X position of the light of power that Thor must reach.
    the variable lightY: the Y position of the light of power that Thor must reach.
    the variable initialTX: the starting X position of Thor.
    the variable initialTY: the starting Y position of Thor.

'''

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.
# ---
# Hint: You can use the debug stream to print initialTX and initialTY, if Thor seems not follow your orders.

# light_x: the X position of the light of power
# light_y: the Y position of the light of power
# initial_tx: Thor's starting X position
# initial_ty: Thor's starting Y position
light_x, light_y, tx, ty = [int(i) for i in input().split()]

# game loop
while True:
    remaining_turns = int(input())  # The remaining amount of turns Thor can move. Do not remove this line.
    sx = 1 # sign in dx
    dx = light_x - tx
    if dx < 0:
        dx = -dx
        sx = -1
    sy = 1 # sign of dy
    dy = light_y - ty
    if dy < 0:
         dy = -dy
         sy = - 1
    mx = 0 # move in x direction
    my = 0 # move in y direction
    
    print(['dir',dx,dy,'T', tx,ty], file=sys.stderr)
    
    if dx > 0:
      mx = 1
      if dy > 0:
        my = 1
        D=1  # SE
      else:
        D = 0 # E
    else:
      if dy > 0:
          my = 1
          D=2 # S
      else:
          break
    
    if sx < 0:
        D = D + 3
    if sy < 0:
        D = D + 6

    print([D, 'sign', sx,sy,'M', mx,my], file=sys.stderr)
        
    DIRS = "E,SE,S,W,SW,S,E,NE,N,W,NW,N".split(',')
    tx = tx + sx*mx
    ty = ty + sy*my
    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)

    # A single line providing the move to be made: N NE E SE S SW W or NW
    print(DIRS[D])
