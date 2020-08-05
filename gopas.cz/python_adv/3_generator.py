from itertools import islice
from random import randint


def fib():
    n1 = 1
    n2 = 1
    yield n1
    yield n2
    while True:
        n1, n2 = n2, n1 + n2
        yield n2


def rand():
    while True:
        yield randint(1, 99)


def rcomp():
    while True:
        yield 100
        yield from islice(rand(), 2)


print(*[x for _, x in zip(range(100), fib())])

print(*islice(rand(), 100))


print(*islice(rcomp(), 100))
