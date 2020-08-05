def secti():
    volano = 1

    def sectiInt(a, b):
        nonlocal volano
        print(volano)
        volano += 1
        return a + b

    return sectiInt


def nasob(a):
    def nasob_int(b):
        return a * b

    return nasob_int


def mul(a):
    return lambda b: a * b


f = secti()
f(1, 2)
f(3, 4)

nasob4 = nasob(4)
print(nasob4(10))

nasob5 = mul(5)
print(nasob5(10))
