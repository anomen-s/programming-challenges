# Context Managers
# methods __enter, __exit__

with open('mesta.csv', 'rt') as f:
    for l in f:
        print(l.rstrip())

try:
    print(f.readline())
except ValueError as e:
    print('Error', e)


print('-'*30)
class ctx_mgr:
    def __enter__(self):
        print('enter')

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('exit', exc_type)

with ctx_mgr() as cm:
    print('cm', id(cm))
    raise ValueError("fake exc")

