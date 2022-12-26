#!/usr/bin/env python3

"""
Pipes & valves network.
Start at AA.
"""
import re


def read_input(final):
    if final:
        fname = 'input'
    else:
        fname = 'input.sample'
    with open(fname, 'rt') as f:
        pattern = re.compile('^Valve ([A-Z]+) has flow rate=(\\d+); tunnels? leads? to valves? ([A-Z, ]+)\\s*$')
        lines = (pattern.match(line) for line in f)
        return [(rec[1], int(rec[2]), [v.strip() for v in rec[3].split(',')]) for rec in lines]


def print_puml(schema):
    print("@startuml")
    for line in schema:
        if line[1]:
            print(f"[{line[0]}] <<{line[1]}>>")
        for target in line[2]:
            print(f"[{line[0]}] --> [{target}]")
    print("@enduml")


def build_graph(schema):
    graph = {}
    live_valves = []
    for v in schema:
        node = {'id': v[0], 'rate': v[1]}
        graph[v[0]] = node
        if v[1] > 0:
            live_valves.append(v[0])

    for v in schema:
        graph[v[0]]['tunnels'] = [graph[target]['id'] for target in v[2]]

    for start in graph:
        node = graph[start]
        graph[node['id']]['paths'] = find_paths(graph, node)

    return graph, live_valves


def find_paths(graph, start):
    # print(start)
    paths = {}
    queue = [(start['id'], [])]
    visited = []
    while len(queue) > 0:
        node_id, path = queue[0]
        node = graph[node_id]
        # print(start['id'], node_id)
        queue = queue[1:]
        visited.append(node_id)
        if len(path) > 0 and node['rate'] > 0:
            paths[node_id] = (len(path), path)
        for n in node['tunnels']:
            if n not in visited:
                queue.append((n, path + [node_id]))
    return paths


def traverse(graph, actors):
    if len(actors) > 1:
        if actors[1][1] > actors[0][1]:
            a_this = 1
            a_other_actor = actors[0]
        else:
            a_this = 0
            a_other_actor = actors[1]
        a_other = [a_other_actor]
        other_score = a_other_actor[3] + graph[a_other_actor[0]]['rate'] * a_other_actor[1]
    else:
        other_score = 0
        a_this = 0
        a_other = []

    current_id, timeout, path, score = actors[a_this]
    curr = graph[current_id]
    curr_score = score + curr['rate'] * timeout
    max_score = curr_score + other_score

    visited = [p for actor in actors for p in actor[2]]

    for n in curr['paths']:
        if n not in visited:
            dist = curr['paths'][n][0]
            if dist < (timeout - 1):
                max_new = traverse(graph, [(n, timeout - dist - 1, path + [n], curr_score)] + a_other)
                max_score = max(max_score, max_new)

    return max_score


def solve(final):
    schema = read_input(final)
    # print_puml(schema)

    graph, live_valves = build_graph(schema)

    # print(*graph.values(), sep='\n')

    print(traverse(graph, [('AA', 30, [], 0)]))

    print(traverse(graph, [('AA', 26, [], 0), ('AA', 26, [], 0)]))


if __name__ == '__main__':
    print("(expected: 1651,  1707)")
    solve(False)
    print('*' * 30)
    print("(expected: 1944, 2679)")
    solve(True)
