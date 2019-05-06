import itertools
import random

from coloring.graph import Graph


def cycle(n):
    """Generate a cycle of length n"""
    g = Graph()
    for i in range(n):
        g.add_vertex(i + 1)
    for i in range(n):
        g.add_edge(i + 1, (i + 1) % n + 1)
    return g


def kneser_graph(n, k):
    """Generate Kneser graph from set of n elements and subsets of k size"""
    elements = list(itertools.combinations(range(n), k))
    random.shuffle(elements)
    subsets = {idx: set(cmb) for idx, cmb in enumerate(elements)}
    g = Graph()

    for vertex, subset in subsets.items():
        g.add_vertex(vertex)
    for vertex1, subset1 in subsets.items():
        for vertex2, subset2 in subsets.items():
            if not subset1.intersection(subset2):
                g.add_edge(vertex1, vertex2)
    return g


def load_dimacs(file_path):
    """Load a graph in DIMACS format from a specified file"""

    def parse_problem_line(g, line, _):
        [_, _, n, m] = line.split(" ")
        for idx in range(1, int(n) + 1):
            g.add_vertex(idx)
        return int(m)

    def parse_edge_line(g, line, edges_left):
        [_, v1, v2] = line.split(" ")
        g.add_edge(int(v1), int(v2))
        return edges_left - 1

    parsers = {
        'p': parse_problem_line,
        'e': parse_edge_line
    }

    g = Graph()
    edges_left = 0
    with open(file_path, 'r') as fd:
        for line in fd:
            head = str(line.split(' ', 1)[0])
            if head in parsers:
                edges_left = parsers[head](g, line, edges_left)
            if edges_left < 0:
                raise ValueError('invalid DIMACS file: too much edges')

    return g
