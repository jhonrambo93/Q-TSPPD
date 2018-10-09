

class AppData:

    # ('id', 'x', 'y', 'q_p', 'q_d')
    nodes = list()

    # ('id_p','id_d','quantity','delivered')
    transfers = list()

    # capacity vehicle
    capacity = 5

    # quantità corrente
    q_d_n = 0

    # nodo corrente che inizialmente è il nodo 0
    current_node = nodes[0]

    # total lenght
    total_lenght = 0
