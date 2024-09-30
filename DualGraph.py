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

    def dfs_color_faces(self, face, available_colors):
        # Create a set to store used colors for this face
        used_colors = set()

        vertices_of_given_face = self.dcel.get_vertices_of_face(face)

        # For each vertex in this face, assign a color
        for vertex in vertices_of_given_face:
            if vertex.color is not None:
                used_colors.add(vertex.color)  # Collect the color of vertices that are already colored

        # Assign the first available color that isn't used by adjacent vertices
        color_index = 0
        for vertex in vertices_of_given_face:
            if vertex.color is None:  # If the vertex is not yet colored
                while available_colors[color_index] in used_colors:
                    color_index += 1
                    color_index %= 3
                vertex.color = available_colors[color_index]
                used_colors.add(vertex.color)  # Mark this color as used for this face

        # Perform DFS on adjacent faces
        for adjacent_face in self.dual_graph[face]:
            if all(vertex.color is not None for vertex in self.dcel.get_vertices_of_face(adjacent_face)):
                continue  # If all vertices of adjacent face are colored, skip it
            self.dfs_color_faces(adjacent_face, available_colors)

    def three_coloring(self):
        """
        Perform three-coloring of the vertices of a triangulated polygon using the dual graph.
        The graph must be represented as an adjacency list of faces, where each face contains three vertices.
        """
        # Define three available colors (represented as integers)
        available_colors = [0, 1, 2]

        # Start DFS from an arbitrary face (choose the first one in the dual_graph)
        starting_face = next(iter(self.dual_graph.keys()))

        # Run DFS coloring on the faces of the triangulated polygon
        self.dfs_color_faces(starting_face, available_colors)

    # def plot_colored_dcel(self):
    #     plt.figure(figsize=(8, 8))
    #
    #     # Define colors corresponding to 0, 1, 2
    #     color_map = {0: 'red', 1: 'green', 2: 'blue'}
    #
    #     # Plot vertices with their assigned colors
    #     for vertex in self.dcel.vertices:
    #         plt.plot(vertex.point.x, vertex.point.y, 'o', color=color_map[vertex.color], markersize=10)  # Color vertex
    #         plt.text(vertex.point.x, vertex.point.y, f"V{vertex.id}", fontsize=9, ha='right')
    #
    #     # Plot edges
    #     for half_edge in self.dcel.half_edges:
    #         origin = self.dcel.vertices[half_edge.origin.id]
    #         destination = self.dcel.vertices[half_edge.next.origin.id]
    #
    #         # Plot the edge between origin and destination
    #         plt.plot([origin.point.x, destination.point.x], [origin.point.y, destination.point.y], 'k-')
    #
    #     # Set equal scaling and remove axis for better visualization
    #     plt.axis('equal')
    #     plt.grid(False)
    #     plt.gca().set_axis_off()  # Hide axes
    #     plt.show()

    def plot_colored_dcel(self):
        plt.figure(figsize=(8, 8))

        # Define colors corresponding to 0, 1, 2
        color_map = {0: 'red', 1: 'green', 2: 'blue'}
        color_names = {0: "Red", 1: "Green", 2: "Blue"}

        # Initialize color count dictionary
        color_count = {0: 0, 1: 0, 2: 0}

        # Plot vertices with their assigned colors and count color frequencies
        for vertex in self.dcel.vertices:
            color_count[vertex.color] += 1  # Count each vertex color
            plt.plot(vertex.point.x, vertex.point.y, 'o', color=color_map[vertex.color], markersize=10)  # Color vertex
            plt.text(vertex.point.x, vertex.point.y, f"V{vertex.id}", fontsize=9, ha='right')

        # Plot edges
        for half_edge in self.dcel.half_edges:
            origin = self.dcel.vertices[half_edge.origin.id]
            destination = self.dcel.vertices[half_edge.next.origin.id]

            # Plot the edge between origin and destination
            plt.plot([origin.point.x, destination.point.x], [origin.point.y, destination.point.y], 'k-')

        # Find the color with the minimum count
        min_color = min(color_count, key=color_count.get)
        min_color_name = color_names[min_color]
        min_color_value = color_map[min_color]
        min_color_count = color_count[min_color]

        # Set equal scaling and remove axis for better visualization
        plt.axis('equal')
        plt.grid(False)
        plt.gca().set_axis_off()  # Hide axes

        # Display the minimum color count at the bottom of the plot
        plt.text(0.5, -0.1,
                 f"The Sufficient number of Vertex Guards required will be {min_color_count} Colored in {min_color_name}",
                 fontsize=12, ha='center', va='center', transform=plt.gca().transAxes)

        # Show a dot representing the minimum color at the bottom
        plt.plot(0.45, -0.1, 'o', color=min_color_value, markersize=12, transform=plt.gca().transAxes)

        # Show the plot
        plt.show()

    def plot_colored_dcel_with_dual_graph(self):
        plt.figure(figsize=(10, 10))

        # Define colors corresponding to 0, 1, 2
        color_map = {0: 'red', 1: 'green', 2: 'blue'}
        color_names = {0: "Red", 1: "Green", 2: "Blue"}

        # Initialize color count dictionary
        color_count = {0: 0, 1: 0, 2: 0}

        # Plot DCEL vertices with their assigned colors and count color frequencies
        for vertex in self.dcel.vertices:
            color_count[vertex.color] += 1  # Count each vertex color
            plt.plot(vertex.point.x, vertex.point.y, 'o', color=color_map[vertex.color], markersize=10)  # Color vertex
            plt.text(vertex.point.x, vertex.point.y, f"V{vertex.id}", fontsize=9, ha='right')

        # Plot DCEL edges
        for half_edge in self.dcel.half_edges:
            origin = self.dcel.vertices[half_edge.origin.id]
            destination = self.dcel.vertices[half_edge.next.origin.id]

            # Plot the edge between origin and destination
            plt.plot([origin.point.x, destination.point.x], [origin.point.y, destination.point.y], 'k-', lw=1)

        # Now, plot the dual graph (centroids of faces and adjacency)
        for face, adjacent_faces in self.dual_graph.items():
            # Plot the centroid of the face as a node of the dual graph
            centroid = face.centroid
            plt.scatter(centroid.x, centroid.y, c='black', zorder=3, s=50)  # Plot centroids as black points

            # Plot edges connecting the centroids of adjacent faces
            for adjacent_face in adjacent_faces:
                adj_centroid = adjacent_face.centroid
                plt.plot([centroid.x, adj_centroid.x], [centroid.y, adj_centroid.y], 'r-', lw=1,
                         label='Dual graph edge')

        # Find the color with the minimum count
        min_color = min(color_count, key=color_count.get)
        min_color_name = color_names[min_color]
        min_color_value = color_map[min_color]
        min_color_count = color_count[min_color]

        # Set equal scaling and remove axis for better visualization
        plt.axis('equal')
        plt.grid(False)
        plt.gca().set_axis_off()  # Hide axes

        # Display the minimum color count at the bottom of the plot
        plt.text(0.5, -0.1,
                 f"The Sufficient number of Vertex Guards required will be {min_color_count}, Colored in {min_color_name}",
                 fontsize=12, ha='center', va='center', transform=plt.gca().transAxes)

        # Show a dot representing the minimum color at the bottom
        plt.plot(0.45, -0.1, 'o', color=min_color_value, markersize=12, transform=plt.gca().transAxes)

        # Show the plot
        plt.show()
