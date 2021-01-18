import random

from model.point_model import Point


class Sheep:

    def __init__(self, init_pos_limit, uid):
        self.position = Point(rand=True, pos_limit=init_pos_limit)
        self.uid = uid
        self.alive = True

    def __init__(self, sheep_position, uid):
        self.position = sheep_position
        self.uid = uid
        self.alive = True

    def move(self, sheep_move_dist):
        if self.alive:
            rand_num = random.randint(0, 3)
            if rand_num == 0:
                self.position.x += sheep_move_dist
            elif rand_num == 1:
                self.position.x += sheep_move_dist
            elif rand_num == 2:
                self.position.y -= sheep_move_dist
            elif rand_num == 3:
                self.position.x -= sheep_move_dist