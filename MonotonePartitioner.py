from elements.StatusTree import StatusTree


def is_left_turn(prev, current, next_vertex):
    """ Determines if the vertices form a left turn (counterclockwise turn) """
    return (next_vertex.point.x - current.point.x) * (prev.point.y - current.point.y) - (
            prev.point.x - current.point.x) * (next_vertex.point.y - current.point.y) > 0


class MonotonePartitioner:
    def __init__(self, dcel):
        self.dcel = dcel  # The DCEL representation of the original polygon
        self.status_tree = StatusTree()  # Status structure (active edges) for the sweep line
        self.vertex_types = {}  # To store classified vertices
        self.new_diagonals = []

    def classify_vertices(self):
        """ Classifies vertices into start, end, split, merge, and regular """
        n = len(self.dcel.vertices)
        for i, vertex in enumerate(self.dcel.vertices):
            prev = self.dcel.vertices[(i - 1 + n) % n]
            next_vertex = self.dcel.vertices[(i + 1) % n]

            if vertex.point.y > prev.point.y and vertex.point.y > next_vertex.point.y:
                if is_left_turn(prev, vertex, next_vertex):
                    self.vertex_types[vertex.id] = 'start'
                else:
                    self.vertex_types[vertex.id] = 'split'
            elif vertex.point.y < prev.point.y and vertex.point.y < next_vertex.point.y:
                if is_left_turn(prev, vertex, next_vertex):
                    self.vertex_types[vertex.id] = 'end'
                else:
                    self.vertex_types[vertex.id] = 'merge'
            elif prev.point.y < vertex.point.y < next_vertex.point.y:
                self.vertex_types[vertex.id] = 'regular_right'
            else:
                self.vertex_types[vertex.id] = 'regular_left'

            # print(f"{vertex} Type: {self.vertex_types[vertex.id]} Prev: {prev} Next: {next_vertex}")

    def perform_sweep_line_partition(self):
        """ Perform the sweep line algorithm to partition the polygon into monotone pieces """
        # Sort vertices by decreasing y-coordinate (and by x if tie)
        sorted_vertices = sorted(self.dcel.vertices, key=lambda p: (-p.point.y, p.point.x))

        # Classify vertices
        self.classify_vertices()

        for vertex in sorted_vertices:
            v_type = self.vertex_types[vertex.id]
            self.status_tree.set_sweep_line_y(vertex.point.y)

            if v_type == 'start':
                self.handle_start_vertex(vertex)
            elif v_type == 'end':
                self.handle_end_vertex(vertex)
            elif v_type == 'split':
                self.handle_split_vertex(vertex)
            elif v_type == 'merge':
                self.handle_merge_vertex(vertex)
            else:
                self.handle_regular_vertex(vertex)

        for (a, b) in self.new_diagonals:
            self.add_diagonal_to_dcel(a, b)

    def handle_start_vertex(self, vertex):
        """ Handle start vertex during the sweep """
        # Find the next edge in the polygon and add it to the status
        print(f"Start vertex at {vertex}")
        edge = vertex.incident_edge
        self.status_tree.insert(edge)
        edge.helper = vertex  # Set helper to the current vertex
        print(f"Adding edge {edge} to Status Tree")

    def handle_end_vertex(self, vertex):
        """ Handle end vertex during the sweep """
        print(f"End vertex at {vertex}")
        edge = vertex.incident_edge.prev
        if edge.helper and self.vertex_types[edge.helper.id] == 'merge':
            self.add_diagonal(edge.helper, vertex)
        self.status_tree.delete(edge)
        print(f"Removing edge {edge} from Status Tree")

    def handle_split_vertex(self, vertex):
        """ Handle split vertex by adding a diagonal """
        # Find the nearest left edge (status structure is sorted by x-coordinates)
        print(f"Spilt Vertex at {vertex}")
        left_edge = self.status_tree.find_left_neighbor(vertex)

        if left_edge:
            # Add a diagonal connecting V to Helper(E)
            self.add_diagonal(left_edge.helper, vertex)
            # Set the new helper for the left edge
            left_edge.helper = vertex

        edge = vertex.incident_edge
        self.status_tree.insert(edge)
        edge.helper = vertex

        print(f"Adding edge {edge} to Status Tree")

    def handle_merge_vertex(self, vertex):
        """ Handle merge vertex by adding a diagonal """
        print(f"Merge Vertex at {vertex}")
        edge = vertex.incident_edge.prev
        if edge and self.vertex_types[edge.helper.id] == 'merge':
            self.add_diagonal(edge.helper, vertex)
        self.status_tree.delete(edge)
        print(f"Removing edge {edge} from Status Tree")

        left_edge = self.status_tree.find_left_neighbor(vertex)
        if left_edge and self.vertex_types[left_edge.helper.id] == 'merge':
            self.add_diagonal(left_edge.helper, vertex)
        left_edge.helper = vertex

    def handle_regular_vertex(self, vertex):
        """ Handle regular vertex during the sweep """
        print(f"Handling regular vertex at {vertex}")
        # Check whether it is on the left or right chain of the polygon
        if self.vertex_types[vertex.id] == 'regular_left':
            print(f"Interior of Polygon lies to the right of the regular vertex")
            edge = vertex.incident_edge.prev
            if edge and self.vertex_types[edge.helper.id] == 'merge':
                self.add_diagonal(edge.helper, vertex)
            self.status_tree.delete(edge)
            print(f"Removing edge {edge} from Status Tree")
            new_edge = vertex.incident_edge
            self.status_tree.insert(new_edge)
            print(f"Adding edge {new_edge} to Status Tree")
            new_edge.helper = vertex
        else:
            print(f"Interior of Polygon lies to the left of the regular vertex")
            edge = self.status_tree.find_left_neighbor(vertex)
            if edge and self.vertex_types[edge.helper.id] == 'merge':
                self.add_diagonal(edge.helper, vertex)
            edge.helper = vertex

    def add_diagonal(self, vertex1, vertex2):
        """ Add a diagonal between two vertices to make the polygon monotone """
        print(f"Adding diagonal between {vertex1} and {vertex2}")
        self.new_diagonals.append((vertex1, vertex2))

    def add_diagonal_to_dcel(self, vertex1, vertex2):
        if vertex1.id < vertex2.id:
            self.dcel.add_diagonal(vertex1, vertex2)
        else:
            self.dcel.add_diagonal(vertex2, vertex1)
