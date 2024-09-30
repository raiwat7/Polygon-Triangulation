from matplotlib import pyplot as plt

from elements import Face
from elements.Point import Point


class DualGraph:
    def __init__(self, dcel):
        """
        Initialize the dual graph with the given DCEL.
        """
        self.dcel = dcel
        self.dual_graph = {}

    def iterate_half_edges_of_face(self, face: Face):
        """
        Iterate over all the half-edges of a given face and get the incident faces
        corresponding to the twin edges.

        Returns:
            twin_faces (set): A set of incident faces corresponding to the twin edges.
        """
        twin_faces = set()

        x_coordinate_sum = 0
        y_coordinate_sum = 0
        count = 0

        # Find the starting half-edge of the face
        start_edge = face.outer_component

        # Start iterating over the half-edges of the face
        current_edge = start_edge
        while True:
            twin_edge = current_edge.twin

            if twin_edge is not None:
                incident_face = twin_edge.incident_face

                # Add the twin's incident face to the set if it exists
                if incident_face is not None and incident_face.id != 0:
                    twin_faces.add(incident_face)

            x_coordinate_sum = x_coordinate_sum + current_edge.origin.point.x
            y_coordinate_sum = y_coordinate_sum + current_edge.origin.point.y
            count += 1

            # Move to the next half-edge in the face
            current_edge = current_edge.next
            if current_edge == start_edge:
                break  # We've completed a loop around the face

        face.centroid = Point(x_coordinate_sum / count, y_coordinate_sum / count)

        return twin_faces

    def build_dual_graph(self):
        """
        Build the dual graph by iterating through each face and connecting adjacent faces
        that share a common edge.
        """
        # Iterate over all faces to build the dual graph
        for face in self.dcel.faces[1:]:
            self.dual_graph[face] = self.iterate_half_edges_of_face(face)

    def get_dual_graph(self):
        """
        Return the dual graph as an adjacency list.
        """
        return self.dual_graph

    def print_dual_graph(self):
        """
        Print the dual graph for easy visualization.
        """
        for face_id, neighbors in self.dual_graph.items():
            print(f"Face {face_id}: Adjacent faces -> {list(neighbors)}")

    def plot_dual_graph(self):
        plt.figure(figsize=(8, 8))

        # Plot the centroids (nodes of the dual graph)
        for face, adjacent_faces in self.dual_graph.items():
            # Plot the node (centroid of the face)
            centroid = face.centroid
            plt.scatter(centroid.x, centroid.y, c='blue')  # Plot centroids as blue points
            plt.text(centroid.x, centroid.y, f'{face.id}', fontsize=12, ha='center')  # Label the face ID

            # Plot edges to adjacent faces
            for adjacent_face in adjacent_faces:
                adj_centroid = adjacent_face.centroid
                plt.plot([centroid.x, adj_centroid.x], [centroid.y, adj_centroid.y], 'k-', lw=1)  # Black edges

        # Display the plot
        plt.title("Dual Graph of Faces")
        plt.xlabel("X Coordinate")
        plt.ylabel("Y Coordinate")
        plt.show()

    def plot_dcel_and_dual_graph(self):
        """
        Plots both the DCEL (vertices and edges) and the dual graph (faces and their adjacency)
        in the same image.
        """

        plt.figure(figsize=(10, 10))

        # Plot DCEL vertices and edges
        for vertex in self.dcel.vertices:
            plt.plot(vertex.point.x, vertex.point.y, 'bo')  # Plot vertex as a blue dot
            plt.text(vertex.point.x, vertex.point.y, f"V{vertex.id}", fontsize=9, ha='right')  # Annotate vertex

        for half_edge in self.dcel.half_edges:
            origin = self.dcel.vertices[half_edge.origin.id]
            destination = self.dcel.vertices[half_edge.next.origin.id]

            # Plot the edge between origin and destination
            plt.plot([origin.point.x, destination.point.x], [origin.point.y, destination.point.y], 'k-',
                     label='DCEL edge')

        # Plot dual graph nodes and edges (faces and adjacency)
        for face, adjacent_faces in self.dual_graph.items():
            # Plot the node (centroid of the face)
            centroid = face.centroid
            plt.scatter(centroid.x, centroid.y, c='red', zorder=3)  # Plot centroids as red points for dual graph
            plt.text(centroid.x, centroid.y, f'{face.id}', fontsize=12, ha='center', color='red')  # Label the face ID

            # Plot edges to adjacent faces
            for adjacent_face in adjacent_faces:
                adj_centroid = adjacent_face.centroid
                plt.plot([centroid.x, adj_centroid.x], [centroid.y, adj_centroid.y], 'r', lw=1, label='Dual graph edge')

        # Set equal scaling and remove axis for better visualization
        plt.axis('equal')
        plt.grid(False)
        plt.gca().set_axis_off()  # Hide axes for clean visualization

        plt.title("DCEL and Dual Graph")
        plt.show()
