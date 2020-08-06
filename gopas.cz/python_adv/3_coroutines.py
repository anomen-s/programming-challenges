import asyncio


async def gen(u=10):
    i = 1
    while i < u:
        yield i * i
        i += 1
        await asyncio.sleep(0.5)


async def asyncfor():
    print([x async for x in gen(4)])


async def bigsum():
    print('before')
    L1 = map(lambda x: x * x, range(1_000_000))
    s = 0
    for x in L1:
        s += x
    print('after')
    return s


async def fakesum():
    print('before')
    await asyncio.sleep(1)
    print('after')


async def main():
    await asyncio.gather(fakesum(), fakesum(), fakesum())


async def mainr():
    await asyncio.gather(bigsum(), bigsum(), bigsum())


asyncio.run(main())

print('*' * 30)

asyncio.run(mainr())

print('*' * 30)

asyncio.run(asyncfor())

# loop = asyncio.get_event_loop()
# loop.run_until_complete(asyncfor())
# loop.close()
