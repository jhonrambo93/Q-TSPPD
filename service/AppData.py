

class AppData:

    total_trasfer: int = 0

    # decido se applicare la funzione 1 o 2 per la greedy by value
    # true = 1
    # false = 2
    f_1: bool = False

    # boolean variable for files generator
    testing: bool = False

    # total deliveries counter
    total_deliveries: int = 0

    # file nodes name
    file_nodes: str = None

    # file transfers name
    file_transfers: str = None

    # ('id', 'x', 'y', 'q_p', 'q_d')
    nodes = []

    # ('id', 'x', 'y', 'q_p', 'q_d')
    initial_nodes = []

    # ('id_p','id_d','quantity','delivered')
    transfers = []

    # capacity vehicle
    capacity = 5

    # quantità effettiva da scaricare
    q_d_n = 0

    # nodo corrente che inizialmente è il nodo 0
    current_node = None

    # total length
    total_length: int

    # nodi che sono nella soluzione
    nodes_in_solution = []

    # greedy_solution's memory
    # node_previous, node_next, border, transfers, load, carico
    steps = []

    # set of steps list
    set_solution = []

    # steps length of set_solution
    len_set_solution = []
