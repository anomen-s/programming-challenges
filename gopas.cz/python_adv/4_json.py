import json

print(json.dumps(["foo", {'bar': ('baz', None, False, 1.0, 2)}]))

print(json.dumps('\u1234'))

print('-' * 30)

print(json.loads('["foo", {"bar":["baz", null, 1.0, 2]}]'))

print('-' * 30)

from io import StringIO
io = StringIO('["streaming API", null]')
print(json.load(io))
