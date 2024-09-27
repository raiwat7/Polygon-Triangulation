import math
import random

import matplotlib.pyplot as plt

from elements.Point import Point


class Polygon:
    def __init__(self, n=None, vertices=None):
        self.n = n if n else len(vertices)
        self.vertices = vertices if vertices else []
        if vertices is None:
            self.random_simple_polygon()

    def random_simple_polygon(self):
        # Generate n random points
        points = [Point(random.randint(-100, 100), random.randint(-100, 100)) for _ in range(self.n)]

        # Find centroid to sort the points by their polar angle relative to the centroid
        centroid_x = sum(p.x for p in points) / self.n
        centroid_y = sum(p.y for p in points) / self.n
        centroid = Point(centroid_x, centroid_y)

        # Sorting points based on the angle with respect to the centroid ensures a simple polygon
        def polar_angle(point):
            return math.atan2(point.y - centroid.y, point.x - centroid.x)

        points.sort(key=polar_angle)

        # Store sorted points as vertices of the polygon
        self.vertices = points

    def get_vertices(self):
        return [(p.x, p.y) for p in self.vertices]

    def display_polygon(self):
        # Extracting x and y coordinates for plotting
        x_coords = [p.x for p in self.vertices] + [self.vertices[0].x]  # Closing the polygon
        y_coords = [p.y for p in self.vertices] + [self.vertices[0].y]  # Closing the polygon

        # Plot the polygon
        plt.figure()
        plt.fill(x_coords, y_coords, edgecolor='black', fill=False)

        # Display the coordinates near each vertex
        for i, vertex in enumerate(self.vertices):
            plt.annotate(f'({vertex.x}, {vertex.y})', (vertex.x, vertex.y), textcoords="offset points", xytext=(5, 5),
                         # Offset from the vertex position
                         ha='center')

        # Hide the x and y axes and the grid lines
        plt.gca().set_axis_off()
        plt.grid(False)

        # Show the plot
        plt.show()

    def calculate_area(self):
        # Using the Shoelace Theorem to calculate area
        n = len(self.vertices)
        area = 0
        for i in range(n):
            x1, y1 = self.vertices[i].x, self.vertices[i].y
            x2, y2 = self.vertices[(i + 1) % n].x, self.vertices[(i + 1) % n].y  # Closing the polygon by wrapping
            area += (x1 * y2) - (x2 * y1)
        return abs(area) / 2
