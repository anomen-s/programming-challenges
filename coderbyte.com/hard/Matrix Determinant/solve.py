'''
Using the Python language, have the function MatrixDeterminant(strArr) read strArr 
which will be an array of integers represented as strings. 
Within the array there will also be "<>" elements which represent break points. 
The array will make up a matrix where the (number of break points + 1) represents the number of rows. 
Here is an example of how strArr may look: ["1","2","<>","3","4"]. 
The contents of this array are row1=[1 2] and row2=[3 4]. 
Your program should take the given array of elements, create the proper matrix, and then calculate the determinant. 

For the example above, your program should return -2. 
If the matrix is not a square matrix, return -1. 
The maximum size of strArr will be a 6x6 matrix. 
The determinant will always be an integer.

'''

def makeMatrix(arr):
  '''
    Make matrix from list.
    Matrix is list of rows, each row is also list
  '''
  rows = []
  row = []
  for el in arr:
    if el == "<>":
      rows.append(row)
      row = []
    else:
      row.append(int(el))
  rows.append(row)
  return rows


def checkMatrix(M):
  '''
    check if matrix is square
  '''
  dim = len(M)
  for row in M:
    if len(row) != dim:
      return False
  return True

def combinations(items, buffer):
    if len(items) == 0:
      yield buffer
    for i in items:
      ir = list(items)
      ir.remove(i)
      buffer.append(i)
      for x in combinations(ir, buffer) : yield x
      buffer.remove(i)
      ir.append(i)
      

def product(M, l):
   '''
     Multiply matrix elements by given combination.
   '''
   r = 1
   for i in range(len(M)):
     r = r * M[i][l[i]]
   return r


def sigma(l):
   '''
     Count number of swaps in this combination.
     It's sum of lengths (number of items - 1) of all chains 
   '''
   v = [False for x in range(len(l))]
   sumLen = 0
   for start in range(len(l)):
     if not v[start]:
       v[start] = True
       chain = l[start]
       chainLen = 0
       while chain != start:
         v[chain] = True
         chain = l[chain]
         chainLen = chainLen + 1
       sumLen = sumLen + chainLen
   if sumLen % 2 == 0:
     return 1
   else:
     return -1



def det(M):
   D = len(M)
   res = [0 for x in xrange(D)]
   d = 0
   for comb in combinations(xrange(D), []):
     p = product(M, comb)
     d = d + sigma(comb) * p
#     print (['T',comb,p , d, sigma(comb)])
   return d

def MatrixDeterminant(strArr): 

  M = makeMatrix(strArr)
  if not checkMatrix(M):
    return '-1'
#  print (det(M))
  return det(M)
    
    
# keep this function call here  
# to see how to enter arguments in Python scroll down
#print MatrixDeterminant(raw_input())  


print MatrixDeterminant([ "1","2","4", "9","<>","2","1","1","7","<>","4","1","1","3","<>","4","3","6","2"])



  