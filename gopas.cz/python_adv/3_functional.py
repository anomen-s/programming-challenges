import functools
import math


# map
import operator

print(*map(lambda x: x ** 2, range(10)))

print(*map(math.radians, range(10)))

# filter
print(*filter(lambda x: x % 3 == 0, range(20)))


# reduce
reduced = functools.reduce(operator.mul, range(1, 10), 1)
print(reduced)
