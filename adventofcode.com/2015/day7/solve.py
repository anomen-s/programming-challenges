#!/usr/bin/env python3
import re

'''
Emulate logical circuit.
Schema of gates is stored as list of [inputs, gate_command, output]
'''

def read_input(final):
  if (final):
    fname = 'input'
  else:
    fname = 'input.sample'
  with open(fname, 'rt') as f:
    lines = [re.match('([a-zA-Z0-9 ]+) -> ([a-z]+)', line.strip()) for line in f]
 
  return [parsecmd(l[1]) + [l[2]] for l in lines]

def parsecmd(cmdstr):
  cmd = cmdstr.split(' ')
  inputs = [c for c in cmd if re.match('[a-z]+',c)]
  return [inputs, cmd] 

def inputs(gate_in, schema):
  """
  Check if all gate inputs are already computed.
  """
  for i in gate_in:
     if i not in schema:
      return False
  return True

def computearg(arg, state):
  if re.match('[0-9]+', arg):
    return int(arg)
  else:
    return state[arg] 

def compute(cmd, state):
  """
  Compute result of the gate
  """
  if len(cmd) == 1:
     return computearg(cmd[0], state)
  if cmd[0] == 'NOT':
     return ~computearg(cmd[1], state)
  if cmd[1] == 'AND':
     return computearg(cmd[0], state) & computearg(cmd[2], state)
  if cmd[1] == 'OR':
     return computearg(cmd[0], state) | computearg(cmd[2], state)
  if cmd[1] == 'LSHIFT':
     return computearg(cmd[0], state) << computearg(cmd[2], state)
  if cmd[1] == 'RSHIFT':
     return computearg(cmd[0], state) >> computearg(cmd[2], state)

  raise Exception("Unhandled gate")

def solve(final, part):
 
  schema = read_input(final)
  run1 = solveschema(schema)

  if part == 1:
    return run1

  b_override = [[], [str(run1['a'])], 'b']

  schema = read_input(final)
  schema2 = [g if g[2] != 'b' else b_override for g in schema]
  run2 = solveschema(schema2)

  return run2

def solveschema(schema):

  state = {}

  #print(schema)

  while len(schema) > 0:
    remschema = []

    for gate in schema:
      if inputs(gate[0], state):
        state[gate[2]] = (compute(gate[1], state) & 0xFFFF)
      else:
        remschema.append(gate) 
    schema = remschema

  return state 

if __name__ == '__main__':
 print('(expected %i)' % -1)
 print(solve(False, 1))
 print('*' * 30)
 print('(expected %i, %i)' % (3176,14710))
 print(solve(True,1)['a'])
 print(solve(True,2)['a'])
