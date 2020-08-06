import cProfile
import time
import pstats
import re

# https://docs.python.org/3/library/profile.html

def bigsum(thread):
    print('before')
    L1 = map(lambda x: x * x, range(1000000))
    s = 0
    for x in L1:
        s += x
    print('after')
    return s


def fakesum():
    print('before')
    time.sleep(1)
    print('after')


cProfile.run("bigsum(100_000)", filename='/tmp/python_adv.profile')
cProfile.run("fakesum()", sort='cumtime')

cProfile.run("re.compile('foo|bar')", sort='cumtime')

print('-'*30)

p = pstats.Stats('/tmp/python_adv.profile')
p.strip_dirs().sort_stats(-1).print_stats()
