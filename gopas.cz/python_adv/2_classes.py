class Osoba:
    def __init__(self, jmeno, vek):
        self.jmeno = jmeno
        self.vek = vek

    # finalized (del Osoba)
    def __del__(self):
        print('konec', self.jmeno)

    # + operator
    def __add__(self, other):
        if type(other) is int:
            return self.vek + other
        if type(other) is Osoba:
            return self.vek + other.vek
        raise TypeError('invalid type')

    # add from right
    def __radd__(self, other):
        return other + self.vek

    def __gt__(self, other):
        return self.vek > other.vek;
    def pozdrav(self):
        print("ahoj", self.jmeno, self.vek)

    def __call__(self, *args, **kwargs):
        print("osoba zavolana:", *args, **kwargs)

jan = Osoba('jan', 30)
jana = Osoba('Jana', 40)

print(jan.vek, jana.vek)

jan.pozdrav()

print('getattr:', getattr(jan, 'vek'))

print('plus Osoba:', jan + jana)

print('plus int:', jan + 4)

try:
    print('plus str:', jan + 'a')
except:
    print('cannot add str')

print('rplus int:', 100 + jan)

print('gt', jan > jana)

jan(33, sep='_')

del jana
