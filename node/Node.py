import math


class Node:

    def __init__(self, id: int, x: float, y: float, q_p=0, q_d=0):
        self.id = id
        self.x = x
        self.y = y
        self.q_p = q_p
        self.q_d = q_d

    def __str__(self):
        out = str(self.id) + " {} {} ".format(self.x, self.y)
        return out


def lenght(node_1: Node, node_2: Node):
    return math.sqrt((node_1.x - node_2.x) ** 2 + (node_1.y - node_2.y) ** 2)
