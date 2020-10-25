import random
from model.point_model import Point


class Wolf:

    def __init__(self):
        self.position = Point()

    def move(self, wolf_move_dist, sheep_list):
        distances = []
        for i in range(len(sheep_list)):
            distances.append([i, self.position.calculate_distance(sheep_list[i].position)])
        print(distances)
        distances.sort(key=lambda n: n[1], reverse=True)
        print(distances)
        print(wolf_move_dist)
        print(distances[0][0])
        print()
        print(sheep_list)
        if (distances[0][1] < wolf_move_dist):
            self.position = sheep_list[distances[0][0]].position
            del sheep_list[distances[0][0]]
        print(sheep_list)
