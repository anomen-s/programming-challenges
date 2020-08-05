m = {}
try:
    m['cz'].append('Praha')
except KeyError:
    m['cz'] = ['Praha']

print(m)

m['sk'].append('Blava')
