# Group ID 14 (21114021 & 21114078) - Ashutosh Kumar and Raiwat Bapat
# Date: September 27 2024
# StatusNode.py : Contains the implementation of the Node object used in the binary search tree for the sweep status structure for Monotone Partitioning.

class StatusNode:
    """ Represents a node in the binary search tree for the sweep status structure """

    def __init__(self, edge):
        self.edge = edge  # The half-edge stored in this node
        self.left = None  # Left child
        self.right = None  # Right child
        self.parent = None  # Parent node
