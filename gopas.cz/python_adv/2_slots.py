class X:
    pass


class Y:
    # list of variables
    __slots__ = ['vek', 'jmeno']


y = Y()

# print(y.vek) # AttributeError

y.vek = 44
print(y.vek)

y.blabla = 44
# print(y.blabla) # AttributeError
