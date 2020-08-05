class Stat:

    def __init__(self, cc):
        self.cc = cc
        self.__i = 101


cz = Stat('CZ')

print(cz.cc)
try:
    print(cz.__i)
except:
    print("__i not accessibe")

print('hack it: ', cz._Stat__i)
