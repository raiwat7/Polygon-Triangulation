class HalfEdge:
    _id_counter = 0  # Class variable to assign unique IDs to half-edges

    def __init__(self):
        self.origin = None  # Vertex where this half-edge starts
        self.twin = None    # The opposite half-edge
        self.next = None    # The next half-edge in the polygon
        self.prev = None    # The previous half-edge in the polygon
        self.incident_face = None  # The face this half-edge borders
        self.id = HalfEdge._id_counter
        HalfEdge._id_counter += 1

    def __repr__(self):
        return f"HalfEdge {self.id}: Origin = {self.origin}"