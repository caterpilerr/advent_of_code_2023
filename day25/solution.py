import random
import networkx as nx

input_file = 'input.txt'
with open(input_file, 'r') as f:
    input = f.readlines()


def parse_input(input):
    nodes = []
    for line in input:
        id, adj = line.split(':')
        id = id.strip()
        adj = set(a.strip() for a in adj.split())
        nodes.append((id, adj))

    return nodes


def part_one():
    nodes = parse_input(input)
    G = nx.Graph()
    for id, _ in nodes:
        G.add_node(id)

    for id, adj in nodes:
        for adj_id in adj:
            G.add_edge(id, adj_id, capacity=1)

    min_cut_value = float('inf')
    min_cut_partition = None
    while True:
        node1 = random.choice(list(G.nodes))
        node2 = random.choice(list(G.nodes))
        if node1 != node2:
            cut_edges, partition = nx.minimum_cut(G, node1, node2)
            if cut_edges < min_cut_value:
                min_cut_value = cut_edges
                min_cut_partition = partition
                if min_cut_value == 3:
                    break

    product = len(min_cut_partition[0]) * len(min_cut_partition[1])

    return product


print(f'Part One: {part_one()}')


def part_two():
    return None


print(f'Part Two: {part_two()}')
