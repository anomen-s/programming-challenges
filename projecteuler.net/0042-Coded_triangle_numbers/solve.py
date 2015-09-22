#!/usr/bin/python3
# -*- coding: utf-8 -*-
#The nth term of the sequence of triangle numbers is given by, tn = ½n(n+1); so the first ten triangle numbers are:
#
#1, 3, 6, 10, 15, 21, 28, 36, 45, 55, ...
#
#By converting each letter in a word to a number corresponding to its alphabetical position and adding these values we form a word value. For example, the word value for SKY is 19 + 11 + 25 = 55 = t10. If the word value is a triangle number then we shall call the word a triangle word.
#
#Using words.txt (right click and 'Save Link/Target As...'), a 16K text file containing nearly two-thousand common English words, how many are triangle words?

import math

def readfile(filename):
    with open(filename, 'r') as f: 
       data = f.read()
       return eval('[' + data + ']')

def makeMap(wordList, result):
    m = 0
    for w in wordList:
      wsum = sum([ord(c.lower())-ord('a')+1 for c in w])
      m = max(m, wsum)
      if not wsum in result:
         result[wsum] = []
      result[wsum].append(w)

    return m
    
def main():

    wordList = readfile('p042_words.txt')
    wordMap = {}
    maxSum = makeMap(wordList, wordMap)
    c = 0
    for n in range(maxSum):
     tn = n*(n+1)//2
     if tn in wordMap:
       print(wordMap[tn])
       c = c + len(wordMap[tn])
    print('result',c)
    
if  __name__ =='__main__':main()
