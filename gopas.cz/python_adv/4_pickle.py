import pickle
import shelve

jmena = 'Petr,Jan,Tomáš'.split(',')

with open('/tmp/jmena.bin', 'wb') as f:
    pickle.dump(jmena, f)
    pickle.dump(0x202073612020, f)
    pickle.dump({k: v for k, v in enumerate(jmena)}, f)

with open('/tmp/jmena.bin', 'rb') as f:
    print(*[pickle.load(f) for _ in range(3)], sep='\n')

print('-' * 30)

# shelve uses dbm database

with shelve.open('/tmp/shelve.bin') as data:
    data['jmeno'] = 'Tomáš'
    data['dict'] = {1: 'erste', 2: 4545}

with shelve.open('/tmp/shelve.bin') as data:
    print(data['jmeno'])
    print(data['dict'])
