import csv
import json
import os

from model.sheep_model import Sheep
from model.wolf_model import Wolf


class Playground:
    sheep_list = None
    wolf = None

    def __init__(self, wolf, sheep):
        self.wolf = wolf
        self.sheep_list = sheep

    def get_alive_sheep_number(self):
        n = 0
        for s in self.sheep_list:
            if s.alive:
                n += 1
        return n


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

    def get_alive_sheep_positions(self):
        temp_sheep = []
        for i in range(len(self.sheep_list)):
            if self.sheep_list[i].alive:
                temp_sheep.append(self.sheep_list[i].position)
        return temp_sheep

    def __init__(self, sheep_move_dist: float, wolf_move_dist: float):
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

    def init_dir(self, directory):
        self.directory = directory

    def init_dir(self, wait):
        self.wait = wait

    def run_round(self, index):
        if self.playground.get_alive_sheep_number() != 0:
            for sheep in self.playground.sheep_list:
                sheep.move(sheep_move_dist=self.sheep_move_dist)

        if self.playground.get_alive_sheep_number() != 0:
            self.playground.wolf.move(wolf_move_dist=self.wolf_move_dist, sheep_list=self.playground.sheep_list)

        sheep_positions = []
        for s in self.playground.sheep_list:
            sheep_positions.append(s.position)
        round_ = {'round_no': index, 'wolf_pos': self.playground.wolf.position, 'sheep_pos': sheep_positions}
        self.rounds.append(round_)

        self.alive_sheep.append([index, self.playground.get_alive_sheep_number()])

        self.round_counter += 1

    def run_rounds(self):
        for i in range(self.round_number):
            self.run_round(i)

        self.write_json()
        self.write_csv()

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