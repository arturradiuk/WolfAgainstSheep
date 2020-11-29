import math
import logging

import random


class Point:
    def __init__(self, rand=False, pos_limit=0):
        if rand == False:
            self.x = 0
            self.y = 0
        else:
            self.x = random.uniform(-pos_limit, pos_limit)
            self.y = random.uniform(-pos_limit, pos_limit)
        log = "Point.__init__(", rand, pos_limit, ") called"
        logging.debug(log)

    def calculate_distance(self, other_point):
        dx = self.x - other_point.x
        dy = self.y - other_point.y
        res = math.sqrt(dx ** 2 + dy ** 2)
        log = "Point.calculate_distance(", other_point, ") called, returned " , res
        logging.debug(log)
        return res

    def __str__(self):
        res = "[" + str(round(self.x, 3)) + ", " + str(round(self.y, 3)) + "]"
        log = "Point.__str__() called, returned " + res
        logging.debug(log)
        return res

    def __repr__(self):
        res = str(self)
        log = "Point.__str__() called, returned " + res
        logging.debug(log)
        return res
