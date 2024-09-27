class Vertex:
    _id_counter = 0  # Class variable to assign unique IDs to vertices

    def __init__(self, point):
        self.point = point  # A Point object
        self.incident_edge = None  # One of the edges connected to this vertex
        self.id = Vertex._id_counter
        Vertex._id_counter += 1

    def __repr__(self):
        return f"Vertex {self.id}: ({self.point.x}, {self.point.y})"
