import copy


class Point:
    def __init__(self, x=0, y=0, rand=False, pos_limit=0):
        self.x = x
        self.y = y


temp = Point(1,2)

temp_2 = copy.copy(temp)
# temp_2 = temp
temp_2.x = 0
print(temp.x)