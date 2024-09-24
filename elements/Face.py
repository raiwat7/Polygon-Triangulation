class Face:
    _id_counter = 0  # Class variable to assign unique IDs to faces

    def __init__(self):
        self.outer_component = None  # A half-edge on the outer boundary
        self.inner_component = None  # A half-edge on the inner boundary (for holes), optional
        self.id = Face._id_counter
        Face._id_counter += 1

    def __repr__(self):
        return f"Face {self.id}"