from node.Node import Node


class Step:

    def __init__(self, current_node: Node, node_previous: Node, node_next: Node, border: list, transfers: list, load: int, carico: int):
        self.current_node = current_node
        self.node_previous = node_previous
        self.node_next = node_next
        self.border = border
        self.transfers = transfers
        self.load = load
        self.carico = carico


    def __str__(self):
        out = " {} {} {} {} {} {} {} ".format(self.current_node, self.node_previous, self.node_next, self.border, self.transfers, self.load, self.carico)
        return out
