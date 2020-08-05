class Mesto:

    def __init__(self, jmeno, obyvatele):
        self.jmeno = jmeno
        self.obyvatele = obyvatele

    def __str__(self):
        return self.jmeno

    # def __repr__(self):
    #     return self.jmeno

    def __lt__(self, other):
        return self.obyvatele < other.obyvatele

    # def __cmp__(self, other):
    #     return cmp(self.obyvatele, other.obyvatele)
    #


class Stat:

    def __init__(self, cc, mesto=None):
        self.cc = cc
        self.mesta = []
        if mesto:
            self.mesta.append(mesto)

    def pridej(self, mesto):
        self.mesta.append(mesto)

    def serazene(self):
        return sorted(self.mesta)

    def __getitem__(self, item):
        return self.mesta[item]

    def __len__(self):
        return len(self.mesta)

    def __str__(self):
        return self.cc + ": " + str([str(x) for x in self.serazene()])
        # return self.cc + ": " + ", ".join(map(lambda m:m.jmeno, self.serazene()))

    def __cmp__(self, other):
        return cmp(cc, other.cc)


def nacti():
    result = {}
    with open('mesta.csv', 'rt') as f:
        for line in f:
            mesto = line.strip().split(',')
            m = Mesto(mesto[1], int(mesto[2]))
            stat = result.setdefault(mesto[0], Stat(mesto[0]))
            stat.pridej(m)
            # print(line)
    return result


staty = nacti()

for cc in sorted(staty):
    print(staty[cc])

print('-' * 30)

print('len', len(staty['CZ']))

for m in staty['CZ']:
    print(m)

# print('-'*30)
#
# D={}
# s=Stat('CZ')
# print(hash(s))
# D[s] = []
# print(D[s])
# print(D[Stat('CZ')])
# print(D)
