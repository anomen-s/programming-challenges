# todo - use dict comprehension

D = {a: b for a, b in zip(range(4), range(3, -1, -1))}
print(D)

# works with duplicates
print({k: v for k, v in [(1, 2), (4, 5), (1, 4)]})

data = list(map(str.strip, open('mesta.csv')))


def field(i):
    return lambda line: line.split(',')[i]


D = {field(0)(a): list(filter(lambda line: (line.split(',')[0] == a), data)) for a in set(map(field(0), data))}
print(D)

print('test', [(k, v) for k, v in (r.split(',')[0:2] for r in data)])

C = {k: [y for x, y in (r.split(',')[0:2] for r in data) if x == k] for k, v in (r.split(',')[0:2] for r in data)}
print(C)

print('**' * 30)
C = [(k, [y for x, y in (r.split(',')[0:2] for r in data) if x == k]) for k, v in (r.split(',')[0:2] for r in data)]
print(C)
