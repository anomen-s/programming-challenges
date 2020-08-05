print('-------- variable scope')

a = 10


def func1():
    print(a)
    # cannot switch to other variable from other scope
    # FAILS: a = 100
    b = 100


def func2():
    global a
    print(a)
    a = 100


print(a)
func1()
print(a)
func2()
print(a)

print('-------- default parameters')


def funkce2(a, b=10, c=[]):
    # c is initialized only once, so changes to c are visible by subsequent calls
    c.append(a)
    print(a + b + len(c))


funkce2(1, 2)
funkce2(10, 2)
funkce2(20, 2)
funkce2(31, 2)
print(funkce2.__defaults__)

print('-------- variable parameters')


def funcVarList(a, *b):
    print(a)
    print(b)


funcVarList(1, 2, 3, 4)


def funcVarDict(a, **b):
    print(a)
    print(b)


funcVarDict('keywords args 1', x1=2, x4=3, y5=4)

D = {'a1': '4', 'y5': '5'}
funcVarDict('keywords args 2', **D)

print('-------- hash (dict keys)')

print(hash((3, 4)))
# list is not hashable
print(hash([3, 4]))
