from elements.DCEL import DCEL, Vertex, HalfEdge, Face, diagonal_exist
from collections import deque


class MonotoneTriangulation:
    def __init__(self, dcel: DCEL):
        self.dcel = dcel  # The DCEL that contains monotone polygons
        self.new_diagonals = []  # List of added diagonals

    def is_convex(self, v1: Vertex, v2: Vertex, v3: Vertex) -> bool:
        """Check if three vertices form a convex angle (counterclockwise turn)"""
        return (v2.point.x - v1.point.x) * (v3.point.y - v1.point.y) - (v2.point.y - v1.point.y) * (v3.point.x - v1.point.x) > 0
            
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
                flag = 1-flag
            elif edge.origin == vertices[-1]:
                vertices[-1].chain_val = 2
                flag = 1-flag
            else:
                edge.origin.chain_val = flag
                

            edge = edge.next
            if edge == start:
                break


        for i in range(2, len(vertices) - 1):
            current_vertex = vertices[i]

            if stack[-1].chain_val != current_vertex.chain_val:
                # Case 1: Current vertex is on the opposite chain
                while len(stack) > 1:
                    top_vertex = stack.pop()
                    self.add_diagonal(current_vertex, top_vertex)
                stack.pop()
                stack.append(vertices[i-1])
                stack.append(vertices[i])
            else:
                # Case 2: Current vertex is on the same chain
                ul = stack.pop()
                u = ul
                while diagonal_exist(u, current_vertex, face):
                    self.add_diagonal(current_vertex, u)
                    u = stack.pop()
                stack.append(u)
                stack.append(current_vertex)
                

        # Connect the last vertex to the rest of the stack
        for i in range(1, len(stack) - 1):
            if diagonal_exist(vertices[-1], stack[i], face):
                self.add_diagonal(vertices[-1], stack[i])
        
        for (a, b) in self.new_diagonals:
            self.add_diagonal_to_dcel(a, b)

    def triangulate(self):
        """
        Main triangulation method. Triangulates each monotone polygon stored as faces in the DCEL.
        """
        monotone_faces = [self.dcel.faces[-1]]  # Skip the first face (external polygon)

        for face in monotone_faces:
            self.triangulate_monotone_polygon(face)
