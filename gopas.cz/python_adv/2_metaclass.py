import collections.abc

class Loadable(type):
    def __init__(cls, classname, bases, dict):
        super().__init__(cls, classname, bases, dict)
        assert hasattr(cls)

class Good(metaclass=Loadable):

    def load(self):
        pass

g = Good()

# isinstance(instance, type)
# issubclass(instance, type)
