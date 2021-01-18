import math
import logging

import random


class Point:
    def __init__(self, x=0, y=0, rand=False, pos_limit=0):
        self.x = x
        self.y = y

        if rand == True:
            self.x = random.uniform(-pos_limit, pos_limit)
            self.y = random.uniform(-pos_limit, pos_limit)

    def calculate_distance(self, other_point):
        dx = self.x - other_point.x
        dy = self.y - other_point.y
        res = math.sqrt(dx ** 2 + dy ** 2)
        return res