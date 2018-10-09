from service.AppData import AppData
from node.Node import Node
import math


# funzione distanza euclidea
def lenght(node_1: Node, node_2: Node) -> float:
	return math.sqrt((node_1.x - node_2.x) ** 2 + (node_1.y - node_2.y) ** 2)


# Funzione ammissibilità nodo successivo
def abmissibility_greedy(node: Node, q: int, nodes_in_solution: list) -> bool:
	if node.q_p == 0 and node.q_d == 0:
		return False
	else:
		# Se metto < invece di <= siamo nel caso in cui il bordo non viene creato, risolvere il problema!???
		if (is_destination(node, nodes_in_solution)) and (q-AppData.q_d_n+node.q_p <= AppData.capacity):
			return True
		else:
			return False


# funzione che controlla se nel nodo corrente devo scaricare
def is_destination(node: Node, nodes_in_solution: list) -> bool:
	AppData.q_d_n = 0
	for n_s in nodes_in_solution:
		for t in AppData.transfers:
			if t.delivered is False and n_s.id == t.id_p:
				if t.id_d == node.id:
					AppData.q_d_n = t.q  # Quantità corretta da scaricare
					return True
	return False


# funzione che verifica la fine della greedy
def complete_deliveries(total_deliveries: int) -> bool:
	if len(AppData.transfers) == total_deliveries:
		return False
	else:
		return True


# funzione che trova il nodo più vicino
def get_nearest_node(border: list, minimum_lenght) -> float:
	for n_f in border:
		l = lenght(AppData.current_node, n_f)
		print(l)
		if minimum_lenght is None:
			minimum_lenght = l
			nearest_n = n_f
		elif l < minimum_lenght:
			minimum_lenght = l
			nearest_n = n_f
	AppData.current_node = nearest_n
	AppData.total_lenght += minimum_lenght
	return nearest_n
