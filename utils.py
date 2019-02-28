from service.AppData import AppData
from node.Node import Node
from transfer.Transfer import Transfer
import math
import matplotlib.pylab as plt
import numpy as np
import random
import copy

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
def length(node_1: Node, node_2: Node) -> float:
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
		l = length(AppData.current_node, n_f)
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
	AppData.total_length += length(AppData.current_node, best_n)
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

	return ((load - scarico + carico) / AppData.capacity) / length(AppData.current_node, n_f)


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
	AppData.total_length += length(AppData.current_node, best_n)
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
	distanza = length(n_f, AppData.current_node)
	#valore finale
	function_value = (transfers_value*1 + furgone_load_value*1)/(distanza*1)

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


# funzione creazione immagini
def images_sol_generation(solution: list):

	# init
	all_nodes = AppData.nodes[:]
	d = all_nodes[0]
	x_max = 0
	y_max = 0

	# linea
	line = [(n.x, n.y) for n in solution]
	line = np.array(line)
	plt.plot(line[:, 0], line[:, 1], linestyle='-', color='green')

	# deposito
	deposito = [(d.x, d.y)]
	deposito = np.array(deposito)
	all_nodes.remove(all_nodes[0])
	# citta
	nodo = [(n.x, n.y) for n in all_nodes]
	nodo = np.array(nodo)
	plt.plot(deposito[0, 0], deposito[0, 1], 'bD', nodo[:, 0], nodo[:, 1], 'ro')

	# configurazione del grafico
	plt.xlabel('X')
	plt.ylabel('Y')
	# imposto le dimensioni del grafico
	for n in AppData.nodes:
		if n.x > x_max:
			x_max = n.x
		if n.y > y_max:
			y_max = n.y
	x_max = x_max * 1.4
	y_max = y_max * 1.4
	plt.axis([0, x_max, 0, y_max])
	plt.axis('on')  # ???
	plt.grid()
	plt.title('Soluzione')
	# creazione immagine grafo
	plt.savefig('images/solution/Final_solution.png')
	# visualizzazione nel video del grafo
	# plt.show()


def project_file_generation():

	nodes = input("\n\nPlease, insert the number of nodes: ")
	x_max = input("Please, insert the maximum value for the X coordinate: ")
	y_max = input("Please, insert the maximum value for the Y coordinate: ")

	if int(x_max) * int(y_max) < int(nodes):
		print("ERROR: the nodes quantity exceeds in the cartesian plane that you created")
	else:  # Nodes file
		file = open("node/n_file/nodesTest.txt", 'w+')
		couples = []
		x_deposito = random.randint(int(x_max)*0.4, int(x_max)*0.6)
		y_deposito = random.randint(int(y_max)*0.4, int(y_max)*0.6)
		file.write('0 ' + str(x_deposito) + ' ' + str(y_deposito) + '\n')
		for i in range(1, int(nodes)):
			file.write(str(i) + ' ')
			while True:
				x = random.randint(0, int(x_max))
				y = random.randint(0, int(y_max))
				if [x, y] not in couples:
					couples.append([x, y])
					break
			file.write(str(x) + ' ' + str(y) + '\n')
		file.close()

		# Transfers file
		file = open("transfer/t_file/transfersTest.txt", 'w+')
		for i in range(1, int(nodes)):
			delivery_nodes = []
			q_tot = 0
			iteration = 0
			while iteration < AppData.capacity:  # un modo come un altro di impedire che tutti i nodi abbiano il massimo di quantitÃ  da consegnare
				candidate_node = random.randint(1, int(nodes) - 1)
				if candidate_node != i:
					if candidate_node not in delivery_nodes:
						quantity = random.randint(1, AppData.capacity)
						q_tot += quantity
						if q_tot <= AppData.capacity:
							delivery_nodes.append(candidate_node)
							file.write(str(i) + ' ' + str(candidate_node) + ' ' + str(quantity) + '\n')
						if q_tot == AppData.capacity:  # sono arrivato al limite --> break e cambio nodo
							break
				iteration += 1
			del delivery_nodes
		file.close()


def border_generation(border: list) -> list:
	for node in AppData.nodes:
		if node.id != 0 and node.id != AppData.current_node.id and abmissibility_greedy(node, AppData.nodes_in_solution):
			border.append(node)

	# to avoid deadlock
	if not border:
		for node in AppData.nodes:
			if node.id != AppData.current_node.id and node.q_p != 0:
				border.append(node)
	return border


# funzione che va a scaricare il furgone
def scarico_node(step: int, load: int, log_file) -> int:

	unload = False
	log_file.write('\nFASE DI SCARICO\n')
	for s in AppData.nodes_in_solution:
		for t in AppData.transfers:
			if (t.id_d == AppData.current_node.id) and (t.delivered is False) and (t.id_p == s.id):
				epsilon = AppData.initial_nodes[t.id_p].q_p - AppData.nodes[t.id_p].q_p
				if epsilon >= t.q:
					load = load - t.q
					AppData.nodes[t.id_p].furgone -= t.q
					AppData.nodes[AppData.current_node.id].q_d -= t.q
					AppData.initial_nodes[t.id_p].q_p -= t.q
					log_file.write('Quantità scaricata = ' + str(t.q) + '\n')
					t.delivered = True
					AppData.steps[step].transfers.append(copy.deepcopy(t))  # Update the task of transfers
					t.q = 0
					AppData.total_deliveries += 1
				else:  # if epsilon < t.q
					load = load - epsilon
					AppData.nodes[t.id_p].furgone -= epsilon
					AppData.nodes[AppData.current_node.id].q_d -= epsilon
					AppData.initial_nodes[t.id_p].q_p -= epsilon
					t.q -= epsilon
					# Update the task of transfers:
					# metto il task in coda ai task dello step
					AppData.steps[step].transfers.append(copy.deepcopy(t))
					# al task corrente vado a mettergli il corretto q rimasto
					AppData.steps[step].transfers[len(AppData.steps[step].transfers) - 1].q = epsilon
					log_file.write('Quantità scaricata = ' + str(epsilon) + '\n')
				unload = True

	if not unload:
		log_file.write('Quantità scaricata = 0 \n')

	return load


# funzione che va a caricare il furgone
def carico_node(step: int, load: int, log_file) -> int:

	log_file.write('FASE DI CARICO' + '\n')
	load += AppData.current_node.q_p
	if load <= AppData.capacity:
		log_file.write('Quantità caricata = ' + str(AppData.nodes[AppData.current_node.id].q_p) + '\n')
		AppData.steps[step].carico = AppData.nodes[AppData.current_node.id].q_p  # Update carico of step
		AppData.nodes[AppData.current_node.id].furgone += AppData.nodes[AppData.current_node.id].q_p
		AppData.nodes[AppData.current_node.id].q_p = 0
	elif load > AppData.capacity:
		scarto = load - AppData.capacity
		load = load - scarto
		carico = AppData.nodes[AppData.current_node.id].furgone = AppData.nodes[AppData.current_node.id].furgone + (AppData.nodes[AppData.current_node.id].q_p - scarto)
		AppData.nodes[AppData.current_node.id].q_p = scarto
		log_file.write('Quantità caricata = ' + str(carico) + '\n')
		AppData.steps[step].carico = carico  # Update carico of step

	return load

