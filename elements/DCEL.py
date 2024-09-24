from Face import Face
from Vertex import Vertex
from HalfEdge import HalfEdge


class DCEL:
    def __init__(self):
        self.vertices = []
        self.half_edges = []
        self.faces = []

    def create_polygon(self, polygon):
        n = len(polygon.vertices)
        if n < 3:
            raise ValueError("A polygon must have at least 3 vertices.")

        # Create a face for the polygon
        face = Face()
        self.faces.append(face)

        unbounded_face = Face()
        self.faces.append(unbounded_face)

        # Create vertices
        dcel_vertices = [Vertex(point) for point in polygon.vertices]
        self.vertices.extend(dcel_vertices)

        # Create half-edges
        half_edges = [HalfEdge() for _ in range(n)]
        twin_half_edges = [HalfEdge() for _ in range(n)]

        # Set up the circular doubly connected edges and their relationships
        for i in range(n):
            next_index = (i + 1) % n
            prev_index = (i - 1 + n) % n

            # Current edge
            half_edges[i].origin = dcel_vertices[i]
            half_edges[i].next = half_edges[next_index]
            half_edges[i].prev = half_edges[prev_index]
            half_edges[i].incident_face = face
            dcel_vertices[i].incident_edge = half_edges[i]

            # Twin edge (opposite direction)
            twin_half_edges[i].origin = dcel_vertices[next_index]
            twin_half_edges[i].next = twin_half_edges[prev_index]
            twin_half_edges[i].prev = twin_half_edges[next_index]
            twin_half_edges[i].incident_face = unbounded_face  # No face, these are outside the polygon
            half_edges[i].twin = twin_half_edges[i]
            twin_half_edges[i].twin = half_edges[i]

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
            print(f"{edge} Previous Edge: {edge.prev} Next Edge: {edge.next} Twin Edge: {edge.twin} Incident Face: {edge.incident_face}")

        # Display faces
        print("\nFaces:")
        for face in self.faces:
            outer = face.outer_component
            inner = face.inner_component
            print(f"{face}: Outer Component Half-Edge: {outer} Inner Component Half-Edge: {inner}")