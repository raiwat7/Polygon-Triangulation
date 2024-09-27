class StatusNode:
    """ Represents a node in the binary search tree for the sweep status structure """

    def __init__(self, edge):
        self.edge = edge  # The half-edge stored in this node
        self.left = None  # Left child
        self.right = None  # Right child
        self.parent = None  # Parent node
