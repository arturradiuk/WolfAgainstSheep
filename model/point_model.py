import math
import random


class Point:
    def __init__(self, rand=False, pos_limit=0):
        if (rand == False):
            self.x = 0
            self.y = 0
        else:
            self.x = random.uniform(-pos_limit, pos_limit)
            self.y = random.uniform(-pos_limit, pos_limit)

    def calculate_distance(self, other_point):
        dx = self.x - other_point.x
        dy = self.y - other_point.y
        return math.sqrt(dx ** 2 + dy ** 2)

    def __str__(self):
        return "[" + str(self.x) + ", " + str(self.y) + "]"
