import os
import time
from multiprocessing import Process, Pool, Lock, Value, set_start_method, Manager

# run method in new process

HELLO = "init"


def f(l, val, name, li, locking):
    if locking: l.acquire()
    global HELLO
    li.append(name)
    for i in range(1000):
        val.value += 1
    print(name, os.getpid(), HELLO)
    # time.sleep(1)
    if locking: l.release()


if __name__ == '__main__':
    # we need to have fork mode to be able to continue in same place in child
    # set_start_method('spawn')
    start = time.perf_counter()
    lock = Lock()
    n = Value('d', 0)
    m = Manager()
    li = m.list()
    print('starting', os.getpid())
    p = [Process(target=f, args=(lock, n, 't-%s' % x, li, True)) for x in range(100)]
    HELLO = "starting"
    [x.start() for x in p]
    print('waiting', os.getpid())
    [x.join() for x in p]
    print('end', os.getpid())
    print('result', n.value)
    print('result', len(li), li)

    exectime = time.perf_counter() - start
    print('time', exectime)

# Pool
print('-'*30)

def getPid(i):
    p = os.getpid()
    time.sleep(.1)
    return 't-%s: %s' % (i, p)

if __name__ == '__main__':
    start = time.perf_counter()

    with Pool(5) as p:
        print(p.map(getPid, [1, 2, 3]))

    exectime = time.perf_counter() - start
    print('time', exectime)
