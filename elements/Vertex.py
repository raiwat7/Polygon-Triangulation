# Group ID 14 (21114021 & 21114078) - Ashutosh Kumar and Raiwat Bapat
# Date: September 24 2024
# Vertex.py : Contains the implementation of the Vertex object of Doubly Connected Edge List (DCEL) data structure.

class Vertex:
    _id_counter = 0  # Class variable to assign unique IDs to vertices

    def __init__(self, point):
        self.point = point  # A Point object
        self.incident_edge = []  # Edges originating from this vertex
        self.id = Vertex._id_counter
        self.chain_val = 0
        self.color = None
        Vertex._id_counter += 1

    def __repr__(self):
        return f"Vertex {self.id}: ({self.point.x}, {self.point.y})"
