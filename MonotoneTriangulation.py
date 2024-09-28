from audioop import reverse

from sympy.physics.units import second

from elements.DCEL import DCEL, Vertex, HalfEdge, Face, diagonal_exist
from collections import deque


class MonotoneTriangulation:
    def __init__(self, dcel: DCEL):
        self.dcel = dcel  # The DCEL that contains monotone polygons
        self.new_diagonals = []  # List of added diagonals

    def add_diagonal(self, vertex1, vertex2):
        """ Add a diagonal between two vertices to make the polygon monotone """
        print(f"Adding diagonal between {vertex1} and {vertex2}")
        self.new_diagonals.append((vertex1, vertex2))

    def add_diagonal_to_dcel(self, vertex1, vertex2):
        if vertex1.id < vertex2.id:
            self.dcel.add_diagonal(vertex1, vertex2)
        else:
            self.dcel.add_diagonal(vertex2, vertex1)

    def triangulate_monotone_polygon(self, face: Face):
        """
        Triangulate a monotone polygon represented by a face in the DCEL.
        """
        # Get the vertices of the face in sorted order by y-coordinate
        vertices = sorted(self.dcel.get_vertices_of_face(face), key=lambda v: (-v.point.y, v.point.x))  # Decreasing y, increasing x
        stack = deque([vertices[0], vertices[1]])  # Initialize stack with first two vertices
        edge = face.outer_component
        start = edge
        flag = 0
        while True:
            if edge.origin == vertices[0]:
                vertices[0].chain_val = 2
                flag = 1 - flag
            elif edge.origin == vertices[-1]:
                vertices[-1].chain_val = 2
                flag = 1 - flag
            else:
                edge.origin.chain_val = flag

            edge = edge.next
            if edge == start:
                break

        for i in range(2, len(vertices) - 1):
            current_vertex = vertices[i]

            if len(stack) > 2:
                top_vertex = stack[-1]
                if top_vertex.chain_val != current_vertex.chain_val:
                    # not_used = []
                    while len(stack) > 1:
                        v = stack.pop()
                        if diagonal_exist(current_vertex, v, face):
                            self.add_diagonal(current_vertex, v)
                    #     else:
                    #         not_used.append(v)
                    # reverse(not_used)
                    # for v in not_used:
                    #
                    stack.append(top_vertex)
                    stack.append(current_vertex)
                else:
                    second_top_vertex = stack[-2]
                    if diagonal_exist(current_vertex, second_top_vertex, face):
                        self.add_diagonal(current_vertex, second_top_vertex)
                        stack.pop()
                        stack.append(current_vertex)
            else:
                second_vertex = stack.pop()
                top_vertex = stack.pop()
                if second_vertex.chain_val != current_vertex.chain_val and diagonal_exist(current_vertex, second_vertex, face):
                    self.add_diagonal(current_vertex, second_vertex)
                    stack.append(second_vertex)
                    stack.append(current_vertex)
                elif diagonal_exist(top_vertex, current_vertex, face):
                    self.add_diagonal(top_vertex, current_vertex)
                    stack.append(top_vertex)
                    stack.append(current_vertex)
                else:
                    stack.append(top_vertex)
                    stack.append(second_vertex)
                    stack.append(current_vertex)

        # Connect the last vertex to the rest of the stack except top & bottom
        for i in range(1, len(stack) - 1):
            if diagonal_exist(vertices[-1], stack[i], face):
                self.add_diagonal(vertices[-1], stack[i])

    def triangulate(self):
        """
        Main triangulation method. Triangulates each monotone polygon stored as faces in the DCEL.
        """
        monotone_faces = self.dcel.faces[1:] # Skip the first face (external polygon)

        for face in monotone_faces:
            self.triangulate_monotone_polygon(face)

        for (a, b) in self.new_diagonals:
            self.add_diagonal_to_dcel(a, b)