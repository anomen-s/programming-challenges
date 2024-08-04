#/usr/bin/env python3

def check(i):
  dprod=1
  t = i
  while t > 0:
    dprod = dprod * (t % 10)
    t = t // 10
  if dprod > 99:
    return False

  p = dprod
  dsum = 0
  while p > 0:
    dsum = dsum + (p % 10)
    p = p // 10

  if (dsum == 9):
    return [i, dprod, dsum]


def check2(abc):
  a = abc // 100
  b = (abc // 10) % 10
  c = abc % 10
  
  if (b-c) < 0:
    return False

  if (2*c-a) < 0:
    return False

  if (2*c-a) > 9:
    return False

  if (b-a) < 0:
    return False

  return True

def coord(abc):
  a = abc // 100
  b = (abc // 10) % 10
  c = abc % 10
  
  n1 = 9-b
  n2 = b-a
  n3 = 2*c-a
  e1 = b-c
  e2=a-2
  return f"(:geo N49°0{n1}.{n2}{n3}0 E020°1{e1}.{e2}{a}0 :)"


for i in range(250, 400):
  c = check(i)
  if c and check2(i):
    res = coord(i)
    print(f"* {c} - {res}")
