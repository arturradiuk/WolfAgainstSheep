from model.sheep_model import Sheep
from model.wolf_model import Wolf
import matplotlib.pyplot as plt


class Playground:  # field for playing
    sheep_list = None
    wolf = None

    def __init__(self, wolf, sheep):
        self.wolf = wolf
        self.sheep_list = sheep

    def get_alive_sheep_number(self):
        n = 0
        for s in self.sheep_list:
            if (s.alive == True):
                n += 1
        return n

    def draw(self):
        for s in self.sheep_list:
            if (s.alive == True):
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

    def run_rounds(self):
        for i in range(self.round_number):
            # self.playground.draw()
            print(
                "-- ", i,
                " -- round start ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print(self.playground.wolf.__str__())

            if (self.playground.get_alive_sheep_number() != 0):
                for sheep in self.playground.sheep_list:
                    sheep.move(sheep_move_dist=self.sheep_move_dist)

            if (self.playground.get_alive_sheep_number() != 0):
                self.playground.wolf.move(wolf_move_dist=self.wolf_move_dist, sheep_list=self.playground.sheep_list)

            print("@ Alive sheep number: ", self.playground.get_alive_sheep_number())
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print("\n")
