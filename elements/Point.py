# Group ID 14 (21114021 & 21114078) - Ashutosh Kumar and Raiwat Bapat
# Date: September 24 2024
# Point.py : Contains the implementation of the Point Object

import math


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance_from_origin(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def __rep__(self):
        return f"Point: ({self.x}, {self.y})"
