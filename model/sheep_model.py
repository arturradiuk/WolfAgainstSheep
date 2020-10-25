import random
from model.point_model import Point


class Sheep:

    def __init__(self, init_pos_limit):
        self.position = Point(rand=True, pos_limit=init_pos_limit)

    def __str__(self) -> str:
        return self.position.__str__()

    # def move(self, sheep_move_dist):
        #         0 - north, 1 - east, 2 - south, 3 - west
        # if (random.randrange(0, 4) == 0):
        #     self.y_pos += sheep_move_dist
        # if (random.randrange(0, 4) == 1):
        #     self.x_pos += sheep_move_dist
        # if (random.randrange(0, 4) == 2):
        #     self.y_pos -= sheep_move_dist
        # if (random.randrange(0, 4) == 3):
        #     self.x_pos -= sheep_move_dist
