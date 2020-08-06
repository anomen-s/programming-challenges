from functools import reduce


def fact(n):
    if n == 1:
        return 1
    return n * fact(n - 1)


def fact_r(n):
    return reduce(lambda x1, x2: x1 * x2, range(1, n+1), 1)


N = 120000

res = fact_r(N)
res2 = None
try:
    res2 = fact(N)
except:
    print('failed')

print((res == res2), res, res2)
