# Group ID 14 (21114021 & 21114078) - Ashutosh Kumar and Raiwat Bapat
# Date: September 24 2024
# Face.py : Contains the implementation of the Face object of Doubly Connected Edge List (DCEL) data structure.

class Face:
    _id_counter = 0  # Class variable to assign unique IDs to faces

    def __init__(self, outer_component=None, inner_component=None):
        self.outer_component = outer_component  # A half-edge on the outer boundary
        self.inner_component = inner_component if inner_component else []  # A half-edge on the inner boundary (for holes), optional
        self.id = Face._id_counter
        self.centroid = None
        Face._id_counter += 1

    def __repr__(self):
        return f"Face {self.id}"
