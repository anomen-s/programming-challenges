class Person:
    Person_id = 1

    def __init__(self, name=None):
        self.__name = name
        self.__age = 0
        self.id = Person.Person_id
        __class__.Person_id += 1

    def resetId(cls):
        cls.Person_id = 1

    resetId = classmethod(resetId)

    #######
    @classmethod
    def incId(cls, inc):
        cls.Person_id += inc

    ######

    @staticmethod
    def getNextId():
        return __class__.Person_id

    #####
    def setname(self, name):
        self.__name = name

    def getname(self):
        return self.__name

    def deletename(selfself):
        del self.__name

    name = property(getname, setname, deletename, "Name property")

    #######

    @property
    def age(self):
        return self.__age

    @age.setter
    def age(self, age):
        if (age < 150) and (age >= 0):
            self.__age = age
        else:
            raise ValueError("Invalid age: " + str(age))

    @age.deleter
    def age(self):
        self.__age = 0;


print([Person().id for i in range(3)])

Person.incId(10)

print([Person().id for i in range(3)])

Person.resetId()

print([Person().id for i in range(3)])

print(Person.getNextId())

print(Person().getNextId())

p1 = Person("P1")
print(p1.name, p1.age)
p1.name = 'P2'
print(p1.name, p1.age)
p1.age = 14
print(p1.name, p1.age)

try:
    p1.age = 214
except ValueError as e:
    print("Error: " + str(e))

del p1.age
print(p1.name, p1.age)


# dynamically create new method
def newMethod(self):
    print('newMethod')


Person.newmeth = newMethod
p1.newmeth()
