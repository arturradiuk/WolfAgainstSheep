from model.point_model import Point
import random
import logging


class Sheep:

    def __init__(self, init_pos_limit, uid):
        self.position = Point(rand=True, pos_limit=init_pos_limit)
        self.uid = uid
        self.alive = True
        log = "Sheep.__init__(", init_pos_limit, uid, ") called"
        logging.debug(log)

    def __init__(self, sheep_position, uid):
        self.position = sheep_position
        self.uid = uid
        self.alive = True


    def move(self, sheep_move_dist):
        if self.alive == True:
            rand_num = random.randint(0, 3)
            if rand_num == 0:
                self.position.x += sheep_move_dist
            elif rand_num == 1:
                self.position.x += sheep_move_dist
            elif rand_num == 2:
                self.position.y -= sheep_move_dist
            elif rand_num == 3:
                self.position.x -= sheep_move_dist

        log = "Sheep.move(", sheep_move_dist, ") called"
        logging.debug(log)

    def __str__(self):
        res = "@ Sheep: uid = " + self.uid.__str__() + "; position = " + self.position.__str__()
        log = "Sheep.move() called, returned ", res
        logging.debug(log)
        return res

    def __repr__(self):
        res = str(self)
        log = "Sheep.move() called, returned ", res
        logging.debug(log)
        return res
