#!/usr/bin/env python3

"""
Compute size of files in directories and search folders by size constraints.
"""


def read_input(final):
    if final:
        fname = 'input'
    else:
        fname = 'input.sample'
    with open(fname, 'rt') as f:
        return [line.split() for line in f]


class Dir:
    def __init__(self):
        self.files = dict()
        self.dirs = dict()
        self.parent = self

    def add_dir(self, name):
        new_dir = Dir()
        new_dir.parent = self
        self.dirs[name] = new_dir

    def add_file(self, name, size):
        self.files[name] = int(size)

    def cd(self, name):
        if name not in self.dirs:
            self.add_dir(name)
        return self.dirs[name]

    def __len__(self):
        return sum(self.files.values()) + sum(len(d) for d in self.dirs.values())

    def caped_size1(self, cap):
        sublen = sum(d.caped_size1(cap) for d in self.dirs.values())
        slen = len(self)
        if slen <= cap:
            return slen + sublen
        else:
            return sublen

    def caped_size2(self, cap):
        max_sub_sizes = sorted(s for s in (d.caped_size2(cap) for d in self.dirs.values()) if s >= cap)

        if max_sub_sizes:
            return max_sub_sizes[0]
        else:
            return len(self)


def build_tree(log):
    tree = Dir()
    current = tree
    for line in log:
        if line[:2] == ['$', 'cd']:
            if line[2] == '/':
                current = tree
            elif line[2] == '..':
                current = current.parent
            else:
                current = current.cd(line[2])
        elif line[0].isnumeric():
            current.add_file(line[1], line[0])
    return tree


def solve(final):
    log = read_input(final)
    tree = build_tree(log)
    used = len(tree)
    needed = used - (70000000 - 30000000)
    print(f'occupied:{used}; to free:{needed}')
    print(tree.caped_size1(100000))
    print(tree.caped_size2(needed))


if __name__ == '__main__':
    print("(expected: 95437, 24933642)")
    solve(False)
    print('*' * 30)
    print("(expected: 919137, 2877389)")
    solve(True)
