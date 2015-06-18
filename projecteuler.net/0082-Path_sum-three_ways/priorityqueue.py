#!/usr/bin/python2
# -*- coding: utf-8 -*-
import Queue


q = Queue.PriorityQueue()

q.put((11,'fabc'))
q.put((1,'abc'))
q.put((1,'abc2'))
q.put((31,'gabc'))

while not q.empty():
  print q.get()[1]

