class Osoba:
    plat = 1000
    def pozdrav(self):
        print('hello ')


jan = Osoba()

jan.pozdrav()

class Osoba:
    def pozdrav(self):
        print('cau')

jana = Osoba()
jana.pozdrav()

robert = jan.__class__()

robert.pozdrav()

jana.jmeno='Jana'
jan.jmeno='Jan'
jan.vek=22
robert.plat=1200

print(dir(jana))
print(dir(jan))

print(jan.plat)
print(robert.plat)
