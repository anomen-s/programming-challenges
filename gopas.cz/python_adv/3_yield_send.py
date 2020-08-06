
def yield_send():
    while True:
        text = (yield)
        if text is None:
            print('none')
            continue
        print('got', text)


ys = yield_send()
x = next(ys)
next(ys)

ys.send('aaa')
ys.send('bbbb')
ys.send('cccc')
