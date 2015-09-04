'''
Using the Python language, have the function SwitchSort(arr) take arr 
which will be an an array consisting of integers 1...size(arr) 
and determine what the fewest number of steps is in order 
to sort the array from least to greatest using the following technique: 
Each element E in the array can swap places with another element 
that is arr[E] spaces to the left or right the chosen element. 
You can loop from one end of the array to the other. 
For example: if arr is the array [1, 3, 4, 2] then you can choose 
the second element which is the number 3, and if you count 3 places 
to the left you'll loop around the array and end up at the number 4. 
Then you swap these elements and arr is then [1, 4, 3, 2]. 
From here only one more step is required, you choose the last element 
which is the number 2, count 2 places to the left and you'll reach the number 4, 
then you swap these elements and you end up with a sorted array [1, 2, 3, 4]. 
Your program should return an integer that specifies the least amount of steps 
needed in order to sort the array using the following switch sort technique.

The array arr will at most contain five elements and will contain at least two elements. 
'''

def isSorted(arr):
    l = -1
    for i in arr:
      if i < l:
        return False
      l = i
    return True

def swap(arr, idx, goLeft):
    distStr = arr[idx]
    dist  = int(distStr)
    if (goLeft):
      neigh = (idx - dist) % len(arr)
    else:
      neigh = (idx + dist) % len(arr)
    arr[idx] = arr[neigh]
    arr[neigh] = distStr
    return arr

def checkVisited(sArr, visitedSet):
  state = ''.join(sArr)
  visited = state in visitedSet
  if not visited:
     visitedSet.add(state)
  return visited
   
def doSwitchSort(queue, visitedSet): 

  while len(queue) > 0:
    (stateStep, state) = queue.pop(0)
    #print [state, stateStep]
    if checkVisited(state, visitedSet):
        continue
    if isSorted(state):
        #print [state, stateStep]
        return stateStep
    for idx in range(len(state)):
      
      stateL = swap(state[:], idx, True)
      #print ['L', idx, stateL, stateStep+1]
      queue.append((stateStep+1, stateL))
      stateR = swap(state[:], idx, False)
      queue.append((stateStep+1, stateR))
      #print ['R', idx,stateR, stateStep+1]


def SwitchSort(arr): 

  sArr = [str(x) for x in  arr]
#  state0 = ''.join(sArr)
  queue = [(0,sArr)]
  visited = set()
  return doSwitchSort(queue, visited)

    
print [0, SwitchSort([1,2,3,4])]
print [3, SwitchSort([3,4,2,1])]
print [2, SwitchSort([1,3,4,2])]
print [4, SwitchSort([5,3,4,1,2])]
print [2, SwitchSort([1, 3, 4, 2])]
print [3,SwitchSort([1, 3, 4, 5, 2])]

# keep this function call here  
# to see how to enter arguments in Python scroll down
print SwitchSort(raw_input())  




