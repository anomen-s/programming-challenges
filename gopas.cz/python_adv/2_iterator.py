class Stat:

    def __init__(self, cc, mesto=None):
        self.cc = cc
        self.mesta = []
        self.inum = 0
        if mesto:
            self.mesta.append(mesto)

    def __iter__(self):
        return self;

    def __next__(self):
        if self.inum < len(self.mesta):
            m = self.mesta[self.inum]
            self.inum = self.inum+1;
            return m
        else:
            raise StopIteration()


s = Stat("CZ",'PRG')

s.mesta.append("HK")

for x in s:
    print(x)
