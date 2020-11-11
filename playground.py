from model.sheep_model import Sheep
from model.wolf_model import Wolf
import matplotlib.pyplot as plt


class Playground:  # field for playing
    sheep_list = None
    wolf = None

    def __init__(self, wolf, sheep):
        self.wolf = wolf
        self.sheep_list = sheep

    def draw(self):
        for s in self.sheep_list:
            plt.scatter(s.position.x, s.position.y, s=100)

        plt.scatter(self.wolf.position.x, self.wolf.position.y, s=1000)

        plt.scatter(-20, 20, s=1)
        plt.scatter(20, 20, s=1)
        plt.scatter(20, -20, s=1)
        plt.scatter(-20, -20, s=1)

        plt.show()


class Simulation:
    def __init__(self, sheep_init_pos_limit, sheep_move_dist, wolf_move_dist, sheep_number, round_number):
        self.sheep_init_pos_limit = sheep_init_pos_limit
        self.sheep_move_dist = sheep_move_dist
        self.wolf_move_dist = wolf_move_dist
        self.sheep_number = sheep_number
        self.round_number = round_number

        wolf = Wolf()
        sheep_list = []
        for i in range(sheep_number):
            sheep_list.append(Sheep(init_pos_limit=10, uid=i))
        self.playground = Playground(wolf, sheep_list)

    def run_round(self):
        self.print_sheep()
        self.print_wolf()
        for sheep in self.playground.sheep_list:
            sheep.move(sheep_move_dist=self.sheep_move_dist)

        self.playground.wolf.move(wolf_move_dist=self.wolf_move_dist, sheep_list=self.playground.sheep_list)

    def run_rounds(self):
        for i in range(self.round_number):
            print "-- ", i, " -- round start ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
            self.print_wolf()
            # self.print_sheep()
            # self.playground.draw()
            for sheep in self.playground.sheep_list:
                sheep.move(sheep_move_dist=self.sheep_move_dist)

            self.playground.wolf.move(wolf_move_dist=self.wolf_move_dist, sheep_list=self.playground.sheep_list)
            print "@ Alive sheep number: ", len(self.playground.sheep_list)
            print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
            print "\n"

    def print_sheep(self):
        print ('\n'.join(map(str, self.playground.sheep_list)))

    def print_wolf(self):
        print (self.playground.wolf.__str__())
