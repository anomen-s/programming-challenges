import re

# functions: search, findall

# re.match searches from start
print(re.match("b", "abc"))
print(re.match("ab", "abc"))

p = re.compile(r'^(.).*\1$')
print(p.search("abeceda"))

p = re.compile(r'[ad]+')
print(p.findall("abeceda"))

print(*p.finditer("abeceda"))


def verify(line):
    # 2letter CC, city, with single space separating words, non-zero population
    # group(3) checks if non-latin char from utf-8 is processed ok
    line_pattern = re.compile(r'^([A-Z]{2}),((\w)\w*(?: \w+)*),([1-9][0-9]+)$')
    m = line_pattern.search(line)
    if m:
        mesto = (m.group(1), m.group(2), m.group(4))
        print(mesto)
    else:
        print('invalid line: <' + line + ">")


with open('mesta.csv', 'rt', encoding='utf-8-sig') as f:
    for line in f:
        # print('<' + line.rstrip() + '>')
        verify(line.rstrip())
