import time
import _thread

def bigsum(thread):
    print('before')
    time.sleep(1)
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

try:
    _thread.start_new_thread(bigsum, ('t1', ))
except:
    pass

while 1:
    pass
