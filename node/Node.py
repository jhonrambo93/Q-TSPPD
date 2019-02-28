

class Node:

    def __init__(self, id: int, x: float, y: float, q_p=0, q_d=0, furgone=0):
        self.id = id
        self.x = x
        self.y = y
        self.q_p = q_p
        self.q_d = q_d
        self.furgone = furgone

    def __str__(self):
        out = str(self.id) + " {} {} {} {} {} ".format(self.x, self.y, self.q_p, self.q_d, self.furgone)
        return out



