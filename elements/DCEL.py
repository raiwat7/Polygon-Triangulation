import math
import random

import matplotlib.pyplot as plt
from tabulate import tabulate

from elements.Face import Face
from elements.HalfEdge import HalfEdge
from elements.Point import Point
from elements.Vertex import Vertex


def diagonal_exist(vertex1, vertex2, face):
    def area_of_triangle2(a, b, c):
        return (b.point.x - a.point.x) * (c.point.y - a.point.y) - (c.point.x - a.point.x) * (b.point.y - a.point.y)

    def left(a, b, c):
        return area_of_triangle2(a, b, c) > 0

    def left_on(a, b, c):
        return area_of_triangle2(a, b, c) >= 0

    def collinear(a, b, c):
        return area_of_triangle2(a, b, c) == 0

    def xor(a, b):
        return a != b

    def proper_intersection(a, b, c, d):
        if collinear(a, b, c) or collinear(a, b, d) or collinear(c, d, a) or collinear(c, d, b):
            return False
        return xor(left(a, b, c), left(a, b, d)) and xor(left(c, d, a), left(c, d, b))

    def between(a, b, c):
        if not collinear(a, b, c):
            return False

        if a.point.x != b.point.x:
            return (a.point.x <= c.point.x <= b.point.x) or (a.point.x >= c.point.x >= b.point.x)
        else:
            return (a.point.y <= c.point.y <= b.point.y) or (a.point.y >= c.point.y >= b.point.y)

    def intersect(a, b, c, d):
        if proper_intersection(a, b, c, d):
            return True
        elif between(a, b, c) or between(a, b, d) or between(c, d, a) or between(c, d, b):
            return True
        else:
            return False

    def diagonalize(a, b, face_queried):
        edge = face_queried.outer_component
        start = edge

        while True:
            if edge.origin != a and edge.origin != b and edge.next.origin != a and edge.next.origin != b and intersect(
                    a, b, edge.origin, edge.next.origin):
                return False

            edge = edge.next
            if edge == start:
                break

        return True

    def in_cone(a, b, face_queried):
        edge = face_queried.outer_component
        start = edge
        prev_vertex = a
        next_vertex = a
        while True:
            if edge.next.origin == a:
                prev_vertex = edge.origin

            if edge.origin == a:
                next_vertex = edge.next.origin
            edge = edge.next
            if edge == start:
                break

        if left_on(a, next_vertex, prev_vertex):
            return left(a, b, prev_vertex) and left(b, a, next_vertex)
        else:
            return not (left_on(a, b, next_vertex) and left_on(b, a, prev_vertex))

    return in_cone(vertex1, vertex2, face) and in_cone(vertex2, vertex1, face) and diagonalize(vertex1, vertex2, face)


class DCEL:
    def __init__(self, n=None, vertices=None, half_edges=None, faces=None):
        self.n = n if n else len(vertices)
        if n is not None:
            self.vertices = []
            self.half_edges = []
            self.faces = []
            self.random_simple_polygon()
        else:
            self.vertices = vertices if vertices else []
            self.half_edges = half_edges if half_edges else []
            self.faces = faces if faces else []

        self.create_polygon()

    def random_simple_polygon(self):
        # Generate n random points
        points = [Point(random.randint(-100, 100), random.randint(-100, 100)) for _ in range(self.n)]

        # Find centroid to sort the points by their polar angle relative to the centroid
        centroid_x = sum(p.x for p in points) / self.n
        centroid_y = sum(p.y for p in points) / self.n
        centroid = Point(centroid_x, centroid_y)

        # Sorting points based on the angle with respect to the centroid ensures a simple polygon
        def polar_angle(vertex):
            return math.atan2(vertex.y - centroid.y, vertex.x - centroid.x)

        points.sort(key=polar_angle)

        for p in points:
            self.vertices.append(Vertex(p))

    def get_vertices(self):
        return [(p.point.x, p.point.y) for p in self.vertices]

    def get_vertices_of_face(self, face: Face):
        """
        Get the vertices in a face in the order they appear along the boundary.
        """
        vertices = []
        edge = face.outer_component
        start = edge

        while True:
            vertices.append(edge.origin)
            edge = edge.next
            if edge == start:
                break

        return vertices

    def are_vertices_in_same_face(self, v1: Vertex, v2: Vertex, face: Face):
        """
        Check if two vertices belong to the same face.
        """
        vertices = self.get_vertices_of_face(face)
        return v1 in vertices and v2 in vertices

    def calculate_area(self):
        # Using the Shoelace Theorem to calculate area
        n = len(self.vertices)
        area = 0
        for i in range(n):
            x1, y1 = self.vertices[i].point.x, self.vertices[i].point.y
            x2, y2 = self.vertices[(i + 1) % n].point.x, self.vertices[
                (i + 1) % n].point.y  # Closing the polygon by wrapping
            area += (x1 * y2) - (x2 * y1)
        return abs(area) / 2

    def create_polygon(self):
        n = len(self.vertices)
        if n < 3:
            raise ValueError("A polygon must have at least 3 vertices.")

        unbounded_face = Face()
        self.faces.append(unbounded_face)

        # Create a face for the polygon
        face = Face()
        self.faces.append(face)

        # Create half-edges
        half_edges = [HalfEdge() for _ in range(n)]
        twin_half_edges = [HalfEdge() for _ in range(n)]

        # Set up the circular doubly connected edges and their relationships
        for i in range(n):
            next_index = (i + 1) % n
            prev_index = (i - 1 + n) % n

            # Current edge
            half_edges[i].origin = self.vertices[i]
            half_edges[i].next = half_edges[next_index]
            half_edges[i].prev = half_edges[prev_index]
            half_edges[i].incident_face = face
            self.vertices[i].incident_edge.append(half_edges[i])

            # Twin edge (opposite direction)
            twin_half_edges[i].origin = self.vertices[(n - i) % n]
            twin_half_edges[i].next = twin_half_edges[next_index]
            twin_half_edges[i].prev = twin_half_edges[prev_index]
            twin_half_edges[i].incident_face = unbounded_face  # No face, these are outside the polygon
            half_edges[i].twin = twin_half_edges[n - i - 1]
            twin_half_edges[n - i - 1].twin = half_edges[i]

        # Connect the face to one of its outer components
        face.outer_component = half_edges[0]
        unbounded_face.inner_component = [twin_half_edges[0]]

        # Add half-edges to the DCEL
        self.half_edges.extend(half_edges)
        self.half_edges.extend(twin_half_edges)

    def display_dcel(self):
        # Display vertices
        print("Vertices:")
        vertex_table = []
        for vertex in self.vertices:
            incident_edges = [edge.id for edge in vertex.incident_edge] if vertex.incident_edge else []
            incident_edges_str = ', '.join(map(str, incident_edges)) if isinstance(incident_edges, list) else "None"
            vertex_table.append([vertex.id, f"({vertex.point.x}, {vertex.point.y})", incident_edges_str])
        print(tabulate(vertex_table, headers=["Vertex ID", "Coordinates", "Incident Edge ID"], tablefmt="grid"))

        # Display half-edges
        print("\nHalfEdges:")
        half_edge_table = []
        for edge in self.half_edges:
            half_edge_table.append(
                [edge.id, edge.origin.id, edge.twin.id if edge.twin else "None", edge.next.id if edge.next else "None",
                 edge.prev.id if edge.prev else "None", edge.incident_face.id if edge.incident_face else "None",
                 edge.helper.id if edge.helper else "None"])
        print(tabulate(half_edge_table,
                       headers=["Half-Edge ID", "Origin Vertex", "Twin Edge ID", "Next Edge ID", "Previous Edge ID",
                                "Incident Face ID", "Edge Helper"], tablefmt="grid"))

        # Display faces
        print("\nFaces:")
        face_table = []
        for face in self.faces:
            outer = face.outer_component.id if face.outer_component else "None"
            inner = [he.id for he in face.inner_component] if face.inner_component else "None"
            # Convert the list of inner component half-edges to a string for display
            inner_str = ', '.join(map(str, inner)) if isinstance(inner, list) else "None"
            face_table.append([face.id, outer, inner_str])
        print(tabulate(face_table, headers=["Face ID", "Outer Component Half-Edge ID", "Inner Component Half-Edge IDs"],
                       tablefmt="grid"))

    def add_diagonal(self, v1, v2):
        """
        Add a diagonal between vertices v1 and v2, updating the DCEL structure.
        This results in the creation of a new face and updating the half-edges and vertices.
        """
        # Step 1: Create two new half-edges for the diagonal
        half_edge_1 = HalfEdge(origin=v1)
        half_edge_2 = HalfEdge(origin=v2)

        # Set twins
        half_edge_1.twin = half_edge_2
        half_edge_2.twin = half_edge_1

        # Step 2: Locate the half-edges around v1 and v2 that will be affected
        # These edges should correspond to the same incident face
        # These half-edges are part of the existing face that will be split
        find_common_incident_edges = lambda v1, v2: next(
            ((e1, e2) for e1 in v1.incident_edge for e2 in v2.incident_edge if
             e1.incident_face.id == e2.incident_face.id), (None, None))
        incident_edge_v1, incident_edge_v2 = find_common_incident_edges(v1, v2)

        # Step 3: Adjust next and prev pointers for the new diagonal edges
        # Find the half-edges that come before and after the new diagonal in the face loop

        half_edge_1.next = incident_edge_v2
        half_edge_2.next = incident_edge_v1

        half_edge_1.prev = incident_edge_v1.prev
        half_edge_2.prev = incident_edge_v2.prev

        incident_edge_v1.prev = half_edge_2
        incident_edge_v2.prev = half_edge_1

        half_edge_1.prev.next = half_edge_1
        half_edge_2.prev.next = half_edge_2

        # Step 4: Create the new face
        new_face = Face(outer_component=half_edge_2)
        self.faces[incident_edge_v2.incident_face.id].outer_component = half_edge_1
        self.faces.append(new_face)

        # Step 5: Update the incident face for the new diagonal half-edges
        half_edge_2.incident_face = new_face
        half_edge_1.incident_face = self.faces[incident_edge_v2.incident_face.id]

        # Update all affected half-edges incident face for the old face
        current_edge = half_edge_2.next
        while current_edge != half_edge_2:
            current_edge.incident_face = half_edge_2.incident_face
            current_edge = current_edge.next

        # Step 7: Add the new half-edges to the DCEL
        self.half_edges.append(half_edge_1)
        self.half_edges.append(half_edge_2)

        v1.incident_edge.append(half_edge_1)
        v2.incident_edge.append(half_edge_2)

    def plot_dcel(self):
        """
        Plots the DCEL with vertex and half-edge annotations.
        Vertices are annotated with their coordinates, and half-edges are annotated with their IDs.
        Handles small edges by adjusting the placement of annotations to avoid overlap.
        """
        plt.figure(figsize=(8, 8))

        # Plot vertices and annotate them
        for vertex in self.vertices:
            plt.plot(vertex.point.x, vertex.point.y, 'bo')  # Plot vertex as a blue dot
            plt.text(vertex.point.x, vertex.point.y, f"V{vertex.id}", fontsize=9, ha='right')

        # Plot edges and annotate half-edges at 1/3rd and 2/3rd points
        for half_edge in self.half_edges:
            origin = self.vertices[half_edge.origin.id]
            destination = self.vertices[half_edge.next.origin.id]

            # Plot the edge between origin and destination
            plt.plot([origin.point.x, destination.point.x], [origin.point.y, destination.point.y], 'k-')

        # Set equal scaling and remove axis for better visualization
        plt.axis('equal')
        plt.grid(False)
        plt.gca().set_axis_off()  # Hide axes
        plt.show()
