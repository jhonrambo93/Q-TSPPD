from service.AppData import AppData
from node.Node import Node
import math


# Euclidean distance function
def lenght(node_1: Node, node_2: Node) -> float:
	return math.sqrt((node_1.x - node_2.x) ** 2 + (node_1.y - node_2.y) ** 2)


# Funzione ammissibilità nodo successivo
def abmissibility_greedy(node: Node, nodes_in_solution: list) -> bool:
	if node.q_p == 0 and node.q_d == 0:
		return False
	else:
		if is_destination(node, nodes_in_solution):
			return True
		else:
			return False


# funzione che controlla se nel nodo corrente devo scaricare
def is_destination(node: Node, nodes_in_solution: list) -> bool:
	AppData.q_d_n = 0  # quantità delivery effettiva
	for n_s in nodes_in_solution:
		for t in AppData.transfers:
			if t.delivered is False and n_s.id == t.id_p and n_s.furgone != 0:
				if t.id_d == node.id:
					# AppData.q_d_n = t.q
					return True
	return False


# funzione che verifica la fine della greedy
def complete_deliveries(total_deliveries: int) -> bool:
	if len(AppData.transfers) == total_deliveries:
		return False
	else:
		return True


# funzione che trova il nodo più vicino
def get_nearest_node(border: list, minimum_length: float) -> Node:
	for n_f in border:
		l = lenght(AppData.current_node, n_f)
		if minimum_length is None:
			minimum_length = l
			nearest_n = n_f
		elif l < minimum_length:
			minimum_length = l
			nearest_n = n_f
	AppData.total_length += minimum_length
	return nearest_n


def get_best_node(border: list, max_value: float, load: int) -> Node:
	for n_f in border:
		value = get_value(n_f, load)
		if max_value is None:
			max_value = value
			best_n = n_f
		elif value > max_value:
			max_value = value
			best_n = n_f
	AppData.total_length += lenght(AppData.current_node, best_n)
	AppData.current_node = best_n
	return best_n


# funzione valore
def get_value(n_f: Node, load: int) -> float:
	scarico = 0
	for s in AppData.nodes_in_solution:
		for t in AppData.transfers:
			if (t.id_d == n_f.id) and (t.delivered is False) and (t.id_p == s.id):
				epsilon = AppData.initial_nodes[t.id_p].q_p - AppData.nodes[t.id_p].q_p
				if epsilon >= t.q:
					scarico =  t.q
				else:
					scarico = epsilon

	q = load - scarico + n_f.q_p
	if q <= AppData.capacity:
		carico = n_f.q_p
	else:
		scarto = q - AppData.capacity
		carico = n_f.q_p - scarto

	return ((load - scarico + carico) / AppData.capacity) / lenght(AppData.current_node, n_f)


# funzione per vedere se un nodo è presente nella soluzione dopo un determinato punto di taglio
def is_next_present(j: int) -> bool:
	counter = 0
	for s in range((j + 1), len(AppData.steps)):
		if AppData.steps[j].current_node == AppData.steps[s].current_node:
			counter += 1
	if counter > 0:
		return True
	else:
		return False


# funzione controllo consegne
def controllo_consegne() -> bool:
	counter_transfer = 0
	for t in AppData.transfers:
		if t.delivered:
			counter_transfer += 1
	if counter_transfer == len(AppData.transfers):
		return True
	else:
		return False


# funzione che trova la soluzione ottima tra le tante ottunute con le euristiche di miglioramento
def get_best_solution() -> (list, float):
	minimum_solution = None
	steps_best_solution = []
	for s in AppData.len_set_solution:
		l = s
		if minimum_solution is None:
			minimum_solution = l
			steps_best_solution = AppData.set_solution[s]
		elif l < minimum_solution:
			minimum_solution = l
			steps_best_solution = AppData.set_solution[s]
	return steps_best_solution, minimum_solution
