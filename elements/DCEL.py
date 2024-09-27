import math
import random

import matplotlib.pyplot as plt

from elements.Face import Face
from elements.HalfEdge import HalfEdge
from elements.Point import Point
from elements.Vertex import Vertex


class DCEL:
    def __init__(self, n=None, vertices=None, half_edges=None, faces=None):
        self.n = n if n else len(vertices)
        if n is not None:
            self.random_simple_polygon()
        else:
            self.vertices = vertices if vertices else []
            self.half_edges = half_edges if half_edges else []
            self.faces = faces if faces else []

            self.create_polygon()

    def random_simple_polygon(self):
        # Generate n random points
        points = [Vertex(Point(random.randint(-100, 100), random.randint(-100, 100))) for _ in range(self.n)]

        # Find centroid to sort the points by their polar angle relative to the centroid
        centroid_x = sum(p.point.x for p in points) / self.n
        centroid_y = sum(p.point.y for p in points) / self.n
        centroid = Vertex(Point(centroid_x, centroid_y))

        # Sorting points based on the angle with respect to the centroid ensures a simple polygon
        def polar_angle(vertex):
            return math.atan2(vertex.point.y - centroid.point.y, vertex.point.x - centroid.point.x)

        points.sort(key=polar_angle)

        # Store sorted points as vertices of the polygon
        self.vertices = points

    def get_vertices(self):
        return [(p.point.x, p.point.y) for p in self.vertices]

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
            self.vertices[i].incident_edge = half_edges[i]

            # Twin edge (opposite direction)
            twin_half_edges[i].origin = self.vertices[(n - i) % n]
            twin_half_edges[i].next = twin_half_edges[next_index]
            twin_half_edges[i].prev = twin_half_edges[prev_index]
            twin_half_edges[i].incident_face = unbounded_face  # No face, these are outside the polygon
            half_edges[i].twin = twin_half_edges[n - i - 1]
            twin_half_edges[n - i - 1].twin = half_edges[i]

        # Connect the face to one of its outer components
        face.outer_component = half_edges[0]
        unbounded_face.inner_component = twin_half_edges[0]

        # Add half-edges to the DCEL
        self.half_edges.extend(half_edges)
        self.half_edges.extend(twin_half_edges)

    def display_dcel(self):
        # Display vertices
        print("Vertices:")
        for vertex in self.vertices:
            print(f"{vertex} Incident Edge: {vertex.incident_edge}")

        # Display half-edges
        print("\nHalfEdges:")
        for edge in self.half_edges:
            print(
                f"{edge} Twin Edge: {edge.twin} Next Edge: {edge.next} Previous Edge: {edge.prev} Incident Face: {edge.incident_face}")

        # Display faces
        print("\nFaces:")
        for face in self.faces:
            outer = face.outer_component
            inner = face.inner_component
            print(f"{face}: Outer Component Half-Edge: {outer} Inner Component Half-Edge: {inner}")

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
        # These half-edges are part of the existing face that will be split
        incident_edge_v1 = v1.incident_edge
        incident_edge_v2 = v2.incident_edge

        # Step 3: Adjust next and prev pointers for the new diagonal edges
        # Find the half-edges that come before and after the new diagonal in the face loop

        # v1 -> v2 (clockwise)
        half_edge_1.next = incident_edge_v2
        half_edge_1.prev = incident_edge_v1.prev

        # v2 -> v1 (counter-clockwise)
        half_edge_2.next = incident_edge_v1
        half_edge_2.prev = incident_edge_v2.prev

        # Adjust the existing half-edges to account for the diagonal
        incident_edge_v1.prev.next = half_edge_1
        incident_edge_v2.prev.next = half_edge_2

        incident_edge_v1.prev = half_edge_2
        incident_edge_v2.prev = half_edge_1

        # Step 4: Create the new face
        new_face = Face(outer_component=half_edge_1)
        self.faces[len(self.faces) - 1].outer_component = half_edge_2
        self.faces.append(new_face)

        # Step 5: Update the incident face for the new diagonal half-edges
        half_edge_1.incident_face = incident_edge_v1.incident_face
        half_edge_2.incident_face = new_face

        # Update all affected half-edges incident face for the new face
        current_edge = half_edge_2.next
        while current_edge != half_edge_2:
            current_edge.incident_face = new_face
            current_edge = current_edge.next

        # Step 6: Update the vertex incident edges
        v1.incident_edge = half_edge_1
        v2.incident_edge = half_edge_2

        # Step 7: Add the new half-edges to the DCEL
        self.half_edges.append(half_edge_1)
        self.half_edges.append(half_edge_2)

    def plot_dcel(self):
        """
        Plots the DCEL with vertex and half-edge annotations.
        Vertices are annotated with their coordinates, and half-edges are annotated with their IDs.
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

            # Calculate the 1/3rd and 2/3rd points of the edge
            third_x = (2 * origin.point.x + destination.point.x) / 3
            third_y = (2 * origin.point.y + destination.point.y) / 3

            plt.text(third_x, third_y, f"HE{half_edge.id}", fontsize=9, color='red')

        # Set equal scaling and remove axis for better visualization
        plt.axis('equal')
        plt.grid(False)
        plt.gca().set_axis_off()  # Hide axes
        plt.show()
