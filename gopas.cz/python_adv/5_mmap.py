import mmap

# open for read and write
with open("mesta.csv", "r+b") as f:
    mapf = mmap.mmap(f.fileno(), 0)

    print(mapf.readline())
    print(mapf[:2])

    print(mapf.tell())
    mapf[3:5] = b"Br"
    mapf.seek(0)

    print(mapf.readline())

    mapf.close()
