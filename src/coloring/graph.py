class Graph:
    """ Graph representation used in the project

    Instead of adjacency matrix or list, this structure stores information
    about edges as a dictionary, where key is a vertex identifiers and value
    is a hash set containing neighbors' identifiers. Despite the memory waste,
    use of sets and dicts implemented with hash tables highly decreases
    the complexity of some operations on sets (union, intersection, difference,
    membership test), which are extensively used in the algorithms from
    `coloring.py` module.

    Basic operations on a graph are still quite efficient:
    - has_vertex - O(1)
    - empty - O(1)
    - add_vertex - O(1)
    - remove_vertex - O(Δ(G))
    - add_edge - O(1)
    - remove_edge - O(1)
    Except for removing the vertex, all of them have constant time complexity.

    Before an edge is inserted, both vertices must already resist in a graph.
    In case of an inconsistent operation is attempted to be executed, GraphError
    is raised with a proper informative message.
    """

    def __init__(self):
        self.vertices = dict()

    def __len__(self):
        return len(self.vertices)

    def has_vertex(self, vertex):
        """Check if Graph has a given vertex"""
        return vertex in self.vertices

    def empty(self):
        """Check if Graph is empty"""
        return len(self.vertices) == 0

    def add_vertex(self, vertex):
        """Add a vertex to Graph"""
        if self.has_vertex(vertex):
            raise GraphError('Graph already has vertex with #%d' % vertex)

        self.vertices[vertex] = set()

    def remove_vertex(self, vertex):
        """Remove a vertex from Graph"""
        if not self.has_vertex(vertex):
            raise GraphError('Graph does not have vertex with #%d' % vertex)

        for neighbor in self.vertices[vertex]:
            self.vertices[neighbor].remove(vertex)
        del self.vertices[vertex]

    def add_edge(self, vertex1, vertex2):
        """Add an edge from Graph"""
        if not self.has_vertex(vertex1):
            raise GraphError('Graph does not have vertex with #%d' % vertex1)
        if not self.has_vertex(vertex2):
            raise GraphError('Graph does not have vertex with #%d' % vertex2)

        if vertex1 not in self.vertices[vertex2]:
            self.vertices[vertex2].add(vertex1)
        if vertex2 not in self.vertices[vertex1]:
            self.vertices[vertex1].add(vertex2)

    def remove_edge(self, vertex1, vertex2):
        """Remove an edge from Graph"""
        if not self.has_vertex(vertex1):
            raise GraphError('Graph does not have vertex with #%d' % vertex1)
        if not self.has_vertex(vertex2):
            raise GraphError('Graph does not have vertex with #%d' % vertex2)

        if vertex1 in self.vertices[vertex2]:
            self.vertices[vertex2].remove(vertex1)
        if vertex2 in self.vertices[vertex1]:
            self.vertices[vertex1].remove(vertex2)


class GraphError(Exception):
    """Exception raised on the invalid operation attempted to be executed on Graph instance"""
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
