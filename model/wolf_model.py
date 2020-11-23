from model.point_model import Point
import math


class Wolf:

    def __init__(self):
        self.position = Point()

    def move(self, wolf_move_dist, sheep_list):
        distances = []

        for i in range(len(sheep_list)):
            if (sheep_list[i].alive == True):
                distances.append([i, self.position.calculate_distance(sheep_list[i].position)])

        if distances.__len__() != 0:
            distances.sort(key=lambda n: n[1], reverse=False)
            if (sheep_list.__len__() != 0):
                if (distances[0][1] < wolf_move_dist):
                    self.position = sheep_list[distances[0][0]].position
                    print (sheep_list[distances[0][0]], " is killed")
                    sheep_list[distances[0][0]].alive = False
                    sheep_list[distances[0][0]].position = None


                else:
                    closest_dist = distances[0][1]
                    w_x = (wolf_move_dist * (
                        math.fabs(sheep_list[distances[0][0]].position.x - self.position.x))) / closest_dist
                    w_y = (wolf_move_dist * (
                        math.fabs(sheep_list[distances[0][0]].position.y - self.position.y))) / closest_dist

                    if sheep_list[distances[0][0]].position.x > 0:  # todo remove duplicates
                        if (self.position.x - sheep_list[distances[0][0]].position.x > 0):
                            self.position.x -= w_x
                        else:
                            self.position.x += w_x
                    else:
                        if (self.position.x - sheep_list[distances[0][0]].position.x > 0):
                            self.position.x -= w_x
                        else:
                            self.position.x += w_x

                    if sheep_list[distances[0][0]].position.y > 0:
                        if (self.position.y - sheep_list[distances[0][0]].position.y > 0):
                            self.position.y -= w_y
                        else:
                            self.position.y += w_y
                    else:
                        if (self.position.y - sheep_list[distances[0][0]].position.y > 0):
                            self.position.y -= w_y
                        else:
                            self.position.y += w_y

    def __str__(self):
        return "# Wolf: position = " + self.position.__str__()

    def __repr__(self):
        return str(self)
