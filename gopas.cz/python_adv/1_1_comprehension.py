from functools import reduce

mesta = {
    'SK': [['SK', 'Zilina', '30000'], ['SK', 'Blava', '450000']],
    'CZ': [['CZ', 'Praha', '1000000']]
}

print('-------- list comprehension ')

print(*[mesta[cc] for cc in mesta if cc != 'CZ'], sep='\n')

print('-------- dictionary comprehension ')

sk = mesta['SK']
print({m: p for (cc, m, p) in sk}, sep='\n')

print('-------- generator expression')

L = range(4)
t = tuple(x ** 3 for x in L)
print(t)

print('-------- nested list comprehension')

L1 = [[1, 2, 3], [4, 5]]
print([x for sublist in L1 for x in sublist])

