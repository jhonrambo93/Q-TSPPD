

class Transfer:
    def __init__(self, id_p: int , id_d: int, q:int, delivered: bool):
        self.id_p = id_p
        self.id_d = id_d
        self.q = q
        self.delivered = delivered

    def __str__(self):
        out = str(self.id) + " {} {} {} {} ".format(self.id_p, self.id_d, self.q, self.delivered)
        return out

