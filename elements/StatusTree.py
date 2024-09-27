from elements.StatusNode import StatusNode


def _find_min(node):
    """ Find the minimum node in the subtree rooted at the given node """
    while node.left:
        node = node.left
    return node


class StatusTree:
    """ Binary search tree (BST) to store the active edges intersecting the sweep line """

    def __init__(self):
        self.root = None  # The root of the tree
        self.sweep_line_y = None  # The current y-coordinate of the sweep line

    def set_sweep_line_y(self, y):
        """ Update the current position of the sweep line """
        self.sweep_line_y = y

    def insert(self, edge):
        """ Insert a new edge into the status tree """
        if not self.root:
            self.root = StatusNode(edge)
        else:
            self._insert_recursive(self.root, edge)

    def _insert_recursive(self, node, edge):
        """ Helper function to recursively insert an edge in the correct position """
        if self.compare_edges(edge, node.edge) < 0:
            if node.left:
                self._insert_recursive(node.left, edge)
            else:
                node.left = StatusNode(edge)
                node.left.parent = node
        else:
            if node.right:
                self._insert_recursive(node.right, edge)
            else:
                node.right = StatusNode(edge)
                node.right.parent = node

    def delete(self, edge):
        """ Remove an edge from the status tree """
        node_to_delete = self._search(self.root, edge)
        if node_to_delete:
            self._delete_node(node_to_delete)

    def _search(self, node, edge):
        """ Search for a node with the given edge """
        if not node or node.edge == edge:
            return node
        if self.compare_edges(edge, node.edge) < 0:
            return self._search(node.left, edge)
        else:
            return self._search(node.right, edge)

    def _delete_node(self, node):
        """ Delete a node from the BST """
        if node.left and node.right:  # Node with two children
            successor = _find_min(node.right)
            node.edge = successor.edge  # Replace with successor's edge
            self._delete_node(successor)
        elif node.left or node.right:  # Node with one child
            child = node.left if node.left else node.right
            self._replace_node(node, child)
        else:  # Node with no children
            self._replace_node(node, None)

    def find_left_neighbor(self, vertex):
        """
        Find the edge immediately to the left of the given vertex V.
        This involves traversing the tree and finding the edge that intersects
        the sweep line and is immediately left of the x-coordinate of the vertex.
        """
        current_node = self.root
        candidate_edge = None

        while current_node:
            edge = current_node.edge
            x_intersection = self.get_x_intersection(edge)

            # If the edge is to the left of the vertex, it could be the candidate
            if x_intersection < vertex.point.x:
                candidate_edge = edge
                current_node = current_node.right  # Search further right
            else:
                current_node = current_node.left  # Search further left

        return candidate_edge  # Return the best candidate found

    def _replace_node(self, node, new_node):
        """ Replace a node with another node in the BST """
        if node.parent:
            if node == node.parent.left:
                node.parent.left = new_node
            else:
                node.parent.right = new_node
        else:
            self.root = new_node
        if new_node:
            new_node.parent = node.parent

    def compare_edges(self, edge1, edge2):
        """ Compare two edges based on their intersection points with the sweep line """
        x1 = self.get_x_intersection(edge1)
        x2 = self.get_x_intersection(edge2)
        if x1 < x2:
            return -1
        elif x1 > x2:
            return 1
        else:
            return 0

    def get_x_intersection(self, edge):
        """ Calculate the x-coordinate where the edge intersects the current sweep line """
        v1, v2 = edge.origin.point, edge.twin.origin.point
        if v1.y == v2.y:
            return v1.x  # Horizontal edge
        slope = (v2.x - v1.x) / (v2.y - v1.y)
        return v1.x + slope * (self.sweep_line_y - v1.y)
