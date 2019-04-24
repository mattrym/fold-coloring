""" Implementation of various algorithms for solving n-fold coloring problem

An implementation is based on heuristic algorithms used in the classical coloring problems.
We modified approximate maximal independent set algorithm, DSATUR algorithm and Connected
Sequential algorithm.

Approximate Maximal Independent Set (AMIS) is choosing a next vertex based on frequency of membership
in a number of various independent sets, which are calculated during the algorithm. Its main purpose
is to vary the shape of maximal independent set, which prevents from achieving a multiplied coloring
(equivalent of classical 1-fold coloring enhanced with color multiplication).

DSATUR is using two approaches: we either find a vertex with a maximum total saturation (total number
of colors assigned to the vertex and its neighbors) with preference to those with smaller inner saturation
(number of colors assigned to a vertex), or we find a vertex with a maximum outer saturation (number of
colors assigned to vertex's neighbors) with preference to those with higher inner saturation.

Connected Sequential algorithm is enhances with color interchange: in case of inability to use a vertex
from the range of colors used before, we try to swap it with some of its neighbors, then swap it with a
neighbor of that neighbor, and so on, until we find a vertex which we can assign a used color without
swapping (or we reach a number of maximum swaps).
"""

import copy
import random


__all__ = [
    'amis_fold_color',
    'total_dsatur_fold_color',
    'outer_dsatur_fold_color',
    'cs_interchange_fold_color'
]


def amis_fold_color(graph, folds=1):
    """ Color properly a graph with n-folds using Approximate Maximum Independent Set

    :param graph: Graph
        graph object
    :param folds: integer
        number of folds
    :return: num_colors, colors : tuple
        number of colors and dict of vertices to set of colors
    """

    frequency = dict()
    colors = dict()

    for vertex in graph.vertices.keys():
        colors[vertex] = set()
        frequency[vertex] = 0

    # find independent set in a graph
    def find_independent_set(graph):
        graph = copy.deepcopy(graph)
        independent_set = set()
        less_rank = True

        def rank(vertex):
            return len(graph.vertices[vertex]) + frequency[vertex]

        while not graph.empty():
            # vertex is chosen alternatively from the most and the least ranked vertices
            index = 0 if less_rank else -1
            less_rank = not less_rank

            # choose vertex from the list of vertices sorted by rank
            vertex = sorted(graph.vertices.keys(), key=rank)[index]
            independent_set.add(vertex)

            # remove vertex with its neighbors from a graph
            neighbors = set(graph.vertices[vertex])
            for neighbor in neighbors:
                graph.remove_vertex(neighbor)
            graph.remove_vertex(vertex)

        # when there are no vertices left, return the set
        return independent_set

    curr_color = 0
    graph = copy.deepcopy(graph)

    while not graph.empty():
        independent_set = find_independent_set(graph)
        curr_color = curr_color + 1

        for vertex in independent_set:
            # color each vertex from independent set with a next color
            colors[vertex].add(curr_color)
            # increase a frequency and remove vertex from graph,
            # if it exceeds the number of folds
            frequency[vertex] = frequency[vertex] + 1
            if frequency[vertex] >= folds:
                graph.remove_vertex(vertex)

    return curr_color, colors


def total_dsatur_fold_color(graph, folds=1):
    """ Color properly a graph with n-folds using DSATUR algorithm with total saturation policy

    :param graph: Graph
        graph object
    :param folds: integer
        number of folds
    :return: num_colors, colors : tuple
        number of colors and dict of vertices to set of colors
    """
    return dsatur_fold_color(graph, folds, saturation='TOTAL')


def outer_dsatur_fold_color(graph, folds=1):
    """ Color properly a graph with n-folds using DSATUR algorithm with outer saturation policy

    :param graph: Graph
        graph object
    :param folds: integer
        number of folds
    :return: num_colors, colors : tuple
        number of colors and dict of vertices to set of colors
    """
    return dsatur_fold_color(graph, folds, saturation='OUTER')


def dsatur_fold_color(graph, folds=1, saturation='TOTAL'):
    colors = dict()
    out_colors = dict()

    for vertex in graph.vertices.keys():
        colors[vertex] = set()
        out_colors[vertex] = set()

    # find vertex with maximum degree
    def find_max_degree_vertex():
        max_degree = 0
        vertices = []

        for vertex, neighbors in graph.vertices.items():
            degree = len(neighbors)
            if degree > max_degree:
                vertices.clear()
                max_degree = degree
            if degree >= max_degree:
                vertices.append(vertex)

        return random.choice(vertices)

    # find vertex with maximum total saturation and minimal inner saturation
    def find_max_total_saturated_degree():
        return max_saturated_vertex(
            calc_first=lambda v: len(out_colors[v]) + len(colors[v]),
            calc_second=lambda v: len(colors[v]),
            cmp_first=lambda maximum, other: maximum - other,
            cmp_second=lambda minimum, other: other - minimum)

    # find vertex with maximum outer saturation and maximum inner saturation
    def find_max_outer_saturated_degree():
        return max_saturated_vertex(
            calc_first=lambda v: len(out_colors[v]),
            calc_second=lambda v: len(colors[v]),
            cmp_first=lambda maximum, other: maximum - other,
            cmp_second=lambda maximum, other: maximum - other)

    # find a maximum saturation from two components (based on given functors and comparers)
    def max_saturated_vertex(calc_first, calc_second, cmp_first, cmp_second):
        m_first = 0
        m_second = 0
        vertices = []

        for vertex in graph.vertices.keys():
            if len(colors[vertex]) >= folds:
                continue
            first = calc_first(vertex)
            second = calc_second(vertex)

            if cmp_first(m_first, first) < 0:
                vertices.clear()
                vertices.append(vertex)
                m_first = first
                m_second = second
            elif cmp_first(m_first, first) == 0:
                if cmp_second(m_second, second) < 0:
                    vertices.clear()
                    vertices.append(vertex)
                    m_second = second
                elif cmp_second(m_second, second) == 0:
                    vertices.append(vertex)

        return random.choice(vertices)

    # choose a maximum finder according to the saturation
    max_finders = {
        'TOTAL': find_max_total_saturated_degree,
        'OUTER': find_max_outer_saturated_degree
    }
    if saturation not in max_finders.keys():
        raise ValueError('unknown comparer: %s' % saturation)
    find_max_saturated_vertex = max_finders[saturation]

    # assign a first color to vertex with the greatest degree
    first_vertex = find_max_degree_vertex()
    first_color = 1
    colors[first_vertex].add(first_color)
    for neighbor in graph.vertices[first_vertex]:
        out_colors[neighbor].add(first_color)

    # for other vertices, find the most saturated vertex
    # and then, color it with the lowest possible color
    colors_left = len(graph.vertices) * folds - 1
    max_color = 0
    while colors_left > 0:
        vertex = find_max_saturated_vertex()
        color = 1
        while color in colors[vertex] or color in out_colors[vertex]:
            color = color + 1

        colors[vertex].add(color)
        for neighbor in graph.vertices[vertex]:
            out_colors[neighbor].add(color)

        if max_color < color:
            max_color = color
        colors_left = colors_left - 1

    return max_color, colors


def cs_interchange_fold_color(graph, folds=1):
    """ Color properly a graph with n-folds using Connected Sequential algorithm with color interchange

    :param graph: Graph
        graph object
    :param folds: integer
        number of folds
    :return: num_colors, colors : tuple
        number of colors and dict of vertices to set of colors
    """

    # find and perform color interchange operations
    # returns:
    #   None - if interchange was not found
    #   colors - if interchange was found
    def color_interchange(vertex):
        tmp_colors = copy.deepcopy(colors)
        analysed_vertices = {vertex}
        current_vertex = vertex

        # find interchange for a given vertex
        def find_interchange(vertex):
            spare_neighbors = set(graph.vertices[vertex])
            spare_neighbors = spare_neighbors.difference(analysed_vertices)

            # considering all the neighbors
            while spare_neighbors:
                chosen_neighbor = random.choice(list(spare_neighbors))
                available_colors = set(tmp_colors[chosen_neighbor])

                # exclude all the colors used already in the target vertex
                # and its neighbors (except for chosen neighbor)
                available_colors = available_colors.difference(tmp_colors[vertex])
                for neighbor in graph.vertices[vertex]:
                    if neighbor != chosen_neighbor:
                        available_colors = available_colors.difference(tmp_colors[neighbor])

                spare_neighbors.remove(chosen_neighbor)

                if available_colors:
                    # exclude neighbor from further analysis (in order to avoid cycles)
                    analysed_vertices.add(chosen_neighbor)
                    return chosen_neighbor, available_colors

            return None

        # try to interchange a color that will result in assigning another color
        # from already used one to the neighbor that we borrow the color from
        # otherwise, choose a color randomly
        def apply_interchange(colors):
            def switch_color(vertex, neighbor, color):
                tmp_colors[vertex].add(color)
                tmp_colors[neighbor].remove(color)

            for color in colors:
                switch_color(current_vertex, chosen_neighbor, color)

                spare_color = find_spare_color(chosen_neighbor)
                if spare_color:
                    tmp_colors[chosen_neighbor].add(spare_color)
                    return True

                switch_color(chosen_neighbor, current_vertex, color)

            color = random.choice(list(colors))
            switch_color(current_vertex, chosen_neighbor, color)
            return False

        # find spare color to replace the interchanged color with it
        def find_spare_color(vertex):
            # find colors which are not used in the vertex and its neighbors
            colors = set(range(1, max_color + 1))
            colors = colors.difference(tmp_colors[vertex])
            for neighbor in graph.vertices[vertex]:
                colors = colors.difference(tmp_colors[neighbor])

            if colors:
                return random.choice(list(colors))

            return None

        for _ in range(len(graph.vertices)):
            # look for neighbor and colors to interchange
            interchange = find_interchange(current_vertex)
            if not interchange:
                break

            # if we interchange one of available colors and replace it
            # with already used one, we return the coloring
            chosen_neighbor, available_colors = interchange
            if apply_interchange(available_colors):
                return tmp_colors

            # if no spare color found, try another interchange
            current_vertex = chosen_neighbor

        return None

    colors = dict()
    for vertex in graph.vertices.keys():
        colors[vertex] = set()
    max_color = 1

    for vertex, neighbors in graph.vertices.items():
        # exclude already used colors for vertex and its neighbors
        available_colors = set(range(1, max_color + 1))
        for neighbor in neighbors:
            available_colors = available_colors.difference(colors[neighbor])

        for _ in range(1, folds + 1):
            if available_colors:
                # find color from used ones
                color = available_colors.pop()
                colors[vertex].add(color)
            else:
                # try interchanging colors
                interchange_result = color_interchange(vertex)
                if interchange_result:
                    colors = interchange_result
                else:
                    # add a new color to scope
                    max_color = max_color + 1
                    colors[vertex].add(max_color)

    return max_color, colors
