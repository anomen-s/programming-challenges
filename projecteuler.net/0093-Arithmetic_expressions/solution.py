#!/usr/bin/python
# -*- coding: utf-8 -*-

import math

PLUS = 0
MUL = 1
DIV = 2
MINUS = 3
OP_COUNT=4

def evalExpr(n1, n2, e):
   ''' evaluate expressions'''
   if e == PLUS:
     return n1 + n2
   elif e == MINUS:
     return n1 - n2
   elif e == MUL:
     return n1 * n2
   elif e == DIV:
     if n2 ==0:
        return None
     return float(n1) / n2
   else:
     raise Exception("Unknown operator: " + e)

def evalB(nums, ops):
    ''' compute (a*b)*(a*b) '''
    l = evalExpr(nums[0], nums[1], ops[0])
    r = evalExpr(nums[2], nums[3], ops[2])
    if (l == None) or (r == None):
      return None
    return evalExpr(l,r, ops[1])

def evalLL(nums, ops):
    ''' compute ((a*b)*a)*b '''
    l = evalExpr(nums[0], nums[1], ops[0])
    if (l == None):
      return None
    l2 = evalExpr(l, nums[2], ops[1])
    if (l2 == None):
     return None
    return evalExpr(l2, nums[3], ops[2])

def evalLR(nums, ops):
    ''' compute (a*(b*a))*b '''
    l = evalExpr(nums[1], nums[2], ops[1])
    if (l == None):
      return None
    l2 = evalExpr(nums[0], l, ops[0])
    if (l2 == None):
      return None
    return evalExpr(l2, nums[3], ops[2])

def evalRR(nums, ops):
    ''' compute a*((b*a)*b) '''
    l = evalExpr(nums[2], nums[3], ops[2])
    if (l == None):
      return None
    l2 = evalExpr(nums[1], l, ops[1])
    if (l2 == None):
      return None
    return evalExpr(nums[0], l2, ops[0])
    
def evalRL(nums, ops):
    ''' compute a*(b*(a*b)) '''
    l = evalExpr(nums[1], nums[2], ops[1])
    if (l == None):
      return None
    l2 = evalExpr(l, nums[3], ops[2])
    if (l2 == None):
      return None
    return evalExpr(nums[0],l2, ops[0])

def nextOp(ops, opcount):
  ''' find next combinations of operators'''
  carry = True
  for i in range(len(ops)):
    if carry:
       carry = False
       r = ops[i] + 1
       if r == opcount:
         r = 0
         carry = True
       ops[i] = r
    else:
      break

  return not carry

def markResult(result, r):
    ''' store result'''
    if (r != None) and (r > 0) and (r % 1 ==  0):
      result[int(r)] = 0
#    else:
#      print 'not mark', r
    
# check all expressions for given number set (no permutation)
def testExpressions(nums, result):
  ops = [0 for i in range(len(nums)-1)]
  while True:
#    print 'check', ops, '=', 'x'
    markResult(result, evalB(nums, ops))
    markResult(result, evalLL(nums, ops))
    if (ops[1] != '+') and (ops[1] != '*'): # skip symetrical cases
     markResult(result, evalLR(nums, ops))
    if (ops[0] != '+') and (ops[0] != '*'): # skip symetrical cases
      markResult(result, evalRL(nums, ops))
      if (ops[1] != '+') and (ops[1] != '*'): # skip symetrical cases
        markResult(result, evalRR(nums, ops))
    
    if not nextOp(ops, OP_COUNT):
#      print 'end', ops
      break

#  test all permutations of given number set
# and return length of generated number squence
#  
def testNumPermutations(numsIn):
   nums = numsIn[:]
   bufferSize=max(nums)**len(nums)
   result = list(range(bufferSize))
   #testExpressions(nums, result)
   for perm in genPermutations(nums, []):
      testExpressions(perm, result)
     
   for r in result:
     if r > 0:
       return r - 1
   raise Exception("Buffer full")

# for each number permutation compute all expressions
def genPermutations(nums, perm):
    if (len(nums) > 1):
      for i in range(len(nums)):
        mynums = nums[:]
        perm.append(mynums.pop(i))
        for n in genPermutations(mynums, perm):
          yield n
        perm.pop()
    else:
#      print 'testing', perm
      yield (perm + nums)
        

# try all 4-digit combinations 
# calls testNumPermutations(selected) for each quartet
def selectNums(numsIn, selected, result):
  if (len(numsIn) == 0) and (len(selected) < 4):
     return
  if len(selected) == 4:
     res = testNumPermutations(selected)
     print (res, selected)
     if res > result[0]:
       result[0] = res
       result[1] = selected[:]
     return
  else:
    first = numsIn[0]
    selected.append(first)
    selectNums(numsIn[1:], selected, result)
    selected.pop()

  selectNums(numsIn[1:], selected, result)
  
#  mynums = numsIn[:]
  
#nums=[1,2,3,4]
#exprList=['+','*','/','#', '_']

#print evalRPN([1,2,4,5,3], '+*+-')
#print nums

#"5 + ((1 + 2) × 4) − 3
#12453 +*+-

#(7+9)/(1/8)
#18 /
#1897 /\*

RESULT = [0,[]]

selectNums([1,2,3,4,5,6,7,8,9], [], RESULT)
print (RESULT)
#print testNumPermutations([1,2,3,4])
