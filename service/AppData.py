

class AppData:

    # ('id', 'x', 'y', 'q_p', 'q_d')
    nodes = []

    # ('id', 'x', 'y', 'q_p', 'q_d')
    initial_nodes = []

    # ('id_p','id_d','quantity','delivered')
    transfers = list()

    # capacity vehicle
    capacity = 5

    # quantità effettiva da scaricare
    q_d_n = 0

    # nodo corrente che inizialmente è il nodo 0
    current_node = None

    # total length
    total_length = 0
