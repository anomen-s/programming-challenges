def secti(a: int, b: int) -> int:
    return a + b


print(secti(1, 2))
print(secti(1, 2.2))
print(secti('a ', ' b'))

print(dir(secti))
print(secti.__annotations__)

i: int = 'fd'

print(i)

print('-' * 30)

import types

# https://docs.python.org/3/library/types.html

from typing import List

Vector = List[float]


def scale(scalar: float, vector: Vector) -> Vector:
    return [scalar * num for num in vector]


# typechecks; a list of floats qualifies as a Vector.
new_vector = scale(2.0, [1, -4.2, 5.4])
print(new_vector)

