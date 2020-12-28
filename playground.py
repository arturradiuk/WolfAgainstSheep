import csv
import json
import logging
import os

import matplotlib.pyplot as plt

from model.sheep_model import Sheep
from model.wolf_model import Wolf


# todo

class Playground:  # field for playing
    sheep_list = None
    wolf = None

    def __init__(self, wolf, sheep):
        self.wolf = wolf
        self.sheep_list = sheep
        log = "Playground.__init__(", self, wolf, sheep, ") called"
        logging.debug(log)

    def get_alive_sheep_number(self):
        n = 0
        for s in self.sheep_list:
            if (s.alive == True):
                n += 1
        log = "Playground.get_alive_sheep_number(", self, ") called, returned ", n
        logging.debug(log)
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
        log = "Playground.draw(", self, ") called"
        logging.debug(log)


class Simulation:

    def set_simulation_parameters(self, sheep_move_dist, wolf_move_dist):
        self.sheep_move_dist = sheep_move_dist
        self.wolf_move_dist = wolf_move_dist

    def remove_sheep(self):
        self.playground.sheep_list.clear()

    def change_wolf_position(self, new_position):
        self.wolf.position = new_position

    def create_sheep(self, sheep_position):
        s = Sheep(sheep_position=sheep_position, uid=self.sheep_counter)
        self.sheep_list.append(s)
        self.sheep_counter += 1

    def get_alive_sheep_positions(self):  # todo
        temp_sheep = []
        for i in range(len(self.sheep_list)):
            if self.sheep_list[i].alive:
                temp_sheep.append(self.sheep_list[i].position)
        return temp_sheep

    def __init__(self, sheep_move_dist: float, wolf_move_dist: float):  # todo
        self.wolf = Wolf()
        self.sheep_list = []
        self.rounds = []
        self.alive_sheep = []

        self.sheep_move_dist = sheep_move_dist
        self.wolf_move_dist = wolf_move_dist
        self.sheep_counter = 0
        self.round_counter = 0

        self.playground = Playground(self.wolf, self.sheep_list)

        self.directory = None
        self.wait = None

    # def init_playground(self):
    #     pass

    def init_dir(self, directory):
        self.directory = directory

    def init_dir(self, wait):
        self.wait = wait

    # def __init__(self, sheep_move_dist: float, wolf_move_dist: float, init_pos_limit: int, sheep_number: int,
    #              round_number, directory: str,
    #              wait: bool):
    #
    #     self.sheep_number = sheep_number
    #     self.round_number = round_number
    #
    #     self.rounds = []
    #     self.alive_sheep = []
    #
    #     wolf = Wolf()
    #     log = "Wolf has been created, the initial position is " + wolf.position.__str__()
    #     logging.info(log)
    #     sheep_list = []
    #     for i in range(sheep_number):
    #         s = Sheep(init_pos_limit=10, uid=i)
    #         sheep_list.append(s)
    #         log = s.uid, " Sheep has been created, the initial position is " + s.position.__str__()
    #         logging.info(log)
    #
    #     self.playground = Playground(wolf, sheep_list)
    #
    #     self.directory = directory
    #     self.wait = wait
    #     log = "Simulation.__init__(", self, init_pos_limit, sheep_move_dist, wolf_move_dist, sheep_number, round_number, directory, wait, ") called"
    #     logging.debug(log)

    def run_round(self, index):
        log = index, " round start"
        logging.info(log)
        # self.playground.draw()  # todo realize as mode
        print(
            "-- ", index,
            " -- round start ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print(self.playground.wolf.__str__())

        if self.playground.get_alive_sheep_number() != 0:
            for sheep in self.playground.sheep_list:
                log = sheep.uid, " sheep maked move from ", sheep.position.__str__()
                sheep.move(sheep_move_dist=self.sheep_move_dist)
                log = log, " to ", sheep.position.__str__()
                logging.info(log)

        if self.playground.get_alive_sheep_number() != 0:
            log = "Wolf maked move from ", self.playground.wolf.position.__str__()
            self.playground.wolf.move(wolf_move_dist=self.wolf_move_dist, sheep_list=self.playground.sheep_list)
            log = log, " to ", self.playground.wolf.position.__str__()
            logging.info(log)

        print("@ Alive sheep number: ", self.playground.get_alive_sheep_number())
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("\n")

        sheep_positions = []
        for s in self.playground.sheep_list:
            sheep_positions.append(s.position)
        round_ = {'round_no': index, 'wolf_pos': self.playground.wolf.position, 'sheep_pos': sheep_positions}
        self.rounds.append(round_)

        self.alive_sheep.append([index, self.playground.get_alive_sheep_number()])

        self.round_counter += 1

        if self.wait:
            os.system('read -sn 1 -p "Press any key to continue..."')

        log = index, " round end"
        logging.info(log)

    def run_rounds(self):

        for i in range(self.round_number):
            self.run_round(i)

        self.write_json()
        self.write_csv()

        log = "Simulation.run_rounds(", self, ") called"
        logging.debug(log)

    def write_json(self):
        self.rounds = json.dumps(self.rounds, default=lambda o: o.__dict__)

        if self.directory:
            if not os.path.exists(self.directory):
                os.mkdir(self.directory)
            os.chdir(self.directory)

            with open('pos.json', 'w') as outfile:
                outfile.write(self.rounds)
            os.chdir('../')
        else:
            with open('pos.json', 'w') as outfile:
                outfile.write(self.rounds)

    def write_csv(self):
        if self.directory:
            if not os.path.exists(self.directory):
                os.mkdir(self.directory)
            os.chdir(self.directory)
            with open('alive.csv', 'w') as file:
                fieldnames = ['round', 'alive_sheep']
                writer = csv.DictWriter(file, fieldnames=fieldnames)

                writer.writeheader()
                for as_ in self.alive_sheep:
                    writer.writerow({'round': as_[0], 'alive_sheep': as_[1]})
        else:
            with open('alive.csv', 'w') as file:
                fieldnames = ['round', 'alive_sheep']
                writer = csv.DictWriter(file, fieldnames=fieldnames)

                writer.writeheader()
                for as_ in self.alive_sheep:
                    writer.writerow({'round': as_[0], 'alive_sheep': as_[1]})
