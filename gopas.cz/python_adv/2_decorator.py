def bold(f1):
    def decF(*args, **kw):
        return "<b>%s</b>" % f1(*args, **kw)

    return decF


# parametrized decorator. return concrete implementation of decorator depending on param
def xitalic(color):
    def concrete_decorator(f1):
        def decF(*args, **kw):
            return "<i color='%s'>%s</i>" % (color, f1(*args, **kw))

        return decF

    return concrete_decorator


# alternative way, using lambda
def color_decorator(f1, color):
    def decF(*args, **kw):
        return "<i color='%s'>%s</i>" % (color, f1(*args, **kw))

    return decF


def italic(color):
    return lambda f: color_decorator(f, color)


####################33

def pozdrav(name):
    return 'ahoj ' + name


myFunc = bold(pozdrav)

print(myFunc('pepa'))


@italic('red')
@bold
def dekorovany_pozdrav(name):
    return 'ahoj ' + name


print(dekorovany_pozdrav('pepa'))

print('-' * 30)
# example of existing decorator (LRU cache)
import functools


@functools.lru_cache()
def secti(a, b):
    print('%i + %i' % (a, b))
    return a + b


print(secti(1, 2))
print(secti(4, 2))
print(secti(1, 2))

print('-' * 30)
# decorator for timing
import time


def timed(f1):
    def decF(*args, **kw):
        start = time.time()
        result = f1(*args, **kw)
        dur = time.time() - start
        print('duration', dur)
        return result

    return decF

@timed
def computation(items):
    L1 = list(range(items))
    x = sum(L1)
    return x


@timed
def computation2(items):
    L1 = list(range(items))
    x = 0
    for i in L1:
        x += i
    return x


print('computation result:', computation(1000_000))
print('computation2 result:', computation2(1000_000))

print('computation result:', computation(10_000_000))
print('computation2 result:', computation2(10_000_000))
