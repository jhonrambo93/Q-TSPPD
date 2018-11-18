from service.AppData import AppData
from node.Node import Node
from transfer.Transfer import Transfer
import math


# read nodes files
def read_nodes_file() -> None:
	f = open(AppData.file_nodes, 'r')
	for line in f:
		parts = line.split()
		AppData.nodes.append(Node(int(parts[0]), float(parts[1]), float(parts[2])))
	# for node in AppData.nodes:
	# print(node)
	f.close()


# read transfers file
def read_transfers_file() -> None:
	f = open(AppData.file_transfers, 'r')
	for line in f:
		parts = line.split()
		AppData.transfers.append(Transfer(int(parts[0]), int(parts[1]), int(parts[2]), False))
	# for transfer in AppData.transfers:
	# print(transfer)
	f.close()


# upgrade nodes list
def upgrade_nodes_list() -> None:
	for node in AppData.nodes:
		if node.id != 0:
			for transfer in AppData.transfers:
				if transfer.id_p == node.id:
					node.q_p = node.q_p + transfer.q
				elif transfer.id_d == node.id:
					node.q_d = node.q_d + transfer.q


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


# funzione che trova il nodo migliore seccondo la funzione get_value
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
	return best_n


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


# funzione che trova il nodo migliore seccondo la funzione get_value_2
def get_best_node_2(border: list, max_value: float, load: int) -> Node:
	for n_f in border:
		value = get_value_2(n_f, load)
		if max_value is None:
			max_value = value
			best_n = n_f
		elif value > max_value:
			max_value = value
			best_n = n_f
	AppData.total_length += lenght(AppData.current_node, best_n)
	return best_n


def get_value_2(n_f: Node, load: int) -> float:
	scarico = 0
	counter: int = 0
	function_value: float = 0
	for s in AppData.nodes_in_solution:
		for t in AppData.transfers:
			if (t.id_d == n_f.id) and (t.delivered is False) and (t.id_p == s.id):
				epsilon = AppData.initial_nodes[t.id_p].q_p - AppData.nodes[t.id_p].q_p
				if epsilon >= t.q:
					scarico = t.q
				else:
					scarico = epsilon
	q = load - scarico + n_f.q_p
	if q <= AppData.capacity:
		carico = n_f.q_p
	else:
		scarto = q - AppData.capacity
		carico = n_f.q_p - scarto

	# conto a quanti nodi deve trasportare il nodo n_f
	for transfer in AppData.transfers:
		if n_f == transfer.id_p and not transfer.delivered:
			counter += 1
	# valore di quanto incidono i trasferimenti che devono ancoara essere eseguiti
	transfers_value = counter/AppData.capacity
	#valore di quanto indide il caricamento completo del furgone
	furgone_load_value = (load - scarico - carico)/AppData.capacity
	# distanza tra i nodi
	distanza = lenght(n_f, AppData.current_node)
	#valore finale
	function_value = (transfers_value*1.5 + furgone_load_value*1)/(distanza*1)

	return function_value


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
def get_best_solution(set_sol: list, len_set_sol: list) -> (list, float):
	minimum_solution = None  # distanza
	steps_best_solution = []  # soluzione
	for s in range(0, len(len_set_sol)):
		l = len_set_sol[s]
		if minimum_solution is None:
			minimum_solution = l
			steps_best_solution = set_sol[s]
		elif l < minimum_solution:
			minimum_solution = l
			steps_best_solution = set_sol[s]
	return steps_best_solution, minimum_solution


