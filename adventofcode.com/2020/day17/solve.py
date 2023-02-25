#!/usr/bin/env python3

"""
3D/4D Game of life
"""

def read_input(final):
    if final:
        fname = 'input'
    else:
        fname = 'input.sample'
    with open(fname, 'rt') as f:
        return [list(line.strip()) for line in f]

def build_neighbours(d4):
    r = set()
    for x in range(-1, 2):
       for y in range(-1, 2):
          for z in range(-1, 2):
             for w in range(-1, 2):
                if x | y | z | (w*d4):
                  r.add((x,y,z,w*d4))
    return r

NEIGH = {3:build_neighbours(0), 4:build_neighbours(1)}

def simulate_step3(space, diameter):
    target = set()
    for x in range(-diameter, diameter+1):
        for y in range(-diameter, diameter+1):
            for z in range(-diameter, diameter+1):
                c = (x,y,z,0)
                n = count_neihgbours(space, c, 3)
                if ((n == 3) or ((n == 2) and (c in space))):
                    target.add(c)  
    return target

def simulate_step4(space, diameter):
    target = set()
    for x in range(-diameter, diameter+1):
        for y in range(-diameter, diameter+1):
            for z in range(-diameter, diameter+1):
                for w in range(-diameter, diameter+1):
                    c = (x,y,z,w)
                    n = count_neihgbours(space, c, 4)
                    if ((n == 3) or ((n == 2) and (c in space))):
                        target.add(c)  
    return target


def count_neihgbours(space, coord, dim):
    r = 0
    for n in NEIGH[dim]:
        ncoord = tuple(a + b for a, b in zip(coord, n))
        r += (ncoord in space)
    return r

def build_space(input):
    space = set()
    w = len(input[0])
    h = len(input)
    for y in range(h):
        for x in range(w):
            if input[y][x] == '#':
                space.add((x-w//2,y-h//2,0,0))
    return space, max(w//2+1, h//2+1)

def compute_sim(space, dim, diameter):

    for step in range(6):
        if dim == 3:
            space = simulate_step3(space, diameter+step)
        else:
            space = simulate_step4(space, diameter+step)

        print(("%s..." % len(space)), end='', flush=True)

    print('|')
    #print(space)
    return len(space)

def solve(final):
    input = read_input(final)
    input_space, diameter = build_space(input)

    compute_sim(input_space, 3, diameter)

    compute_sim(input_space, 4, diameter)

if __name__ == '__main__':
    print("(expected: 112 848)")
    solve(False)
    print('*' * 30)
    print("(expected: 317 1692)")
    solve(True)
