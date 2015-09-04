'''
Have the function SecondGreatLow(arr) take the array of numbers stored in arr 
and return the second lowest and second greatest numbers, 
respectively, separated by a space. 

For example: if arr contains [7, 7, 12, 98, 106] the output should be 12 98. 
The array will not be empty and will contain at least 2 numbers. 
It can get tricky if there's just two numbers! 
'''
def SecondGreatLow(arr): 
  numset = set(arr)
  numlist = list(numset)
  numlist.sort()
  if len(numlist) == 1:
    numlist.append(numlist[0])
  return str(numlist[1]) + ' ' + str(numlist[-2])
        
# keep this function call here  
# to see how to enter arguments in Python scroll down
print SecondGreatLow(raw_input())           
