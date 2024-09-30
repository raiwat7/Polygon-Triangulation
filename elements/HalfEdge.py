class HalfEdge:
    _id_counter = 0  # Class variable to assign unique IDs to half-edges

    def __init__(self, origin=None, twin=None, next_edge=None, prev=None, incident_face=None):
        self.origin = origin  # Vertex where this half-edge starts
        self.twin = twin  # The opposite half-edge
        self.next = next_edge  # The next half-edge in the polygon
        self.prev = prev  # The previous half-edge in the polygon
        self.incident_face = incident_face  # The face this half-edge borders
        self.helper = None
        self.id = HalfEdge._id_counter
        HalfEdge._id_counter += 1

    def __repr__(self):
        return f"HalfEdge {self.id}: Origin = {self.origin}"
