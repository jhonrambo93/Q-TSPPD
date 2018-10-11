from service.AppData import AppData
from node.Node import Node
import utils
import copy


class MenuHandler:

	def serve(self, choice: str) -> None:

		if choice == "GREEDY":

			# initialization
			step = 0
			border = []  # possibili nodi raggiungibili
			solution = []  # elenco dei nodi che compongono la soluzione, cioè il viaggio del furgoncino
			nodes_in_solution = []  # nodi che sono nella soluzione
			total_deliveries = 0  # totale consegne portate a termine
			load = 0  # carico nel furgone
			scaricato = bool  # serve per stampare a video scaricato
			minimum_length = None
			AppData.initial_nodes = copy.deepcopy(AppData.nodes) # copio la lista nodes in initial_nodes

			# Start Greedy
			# Step 0
			AppData.current_node = AppData.nodes[0]  # impongo che il nodo iniziale è il nodo 0
			solution.append(AppData.current_node)

			# Step 1
			step += 1
			print('\nStep ' + str(step))
			for node in AppData.nodes:
				if node.q_p != 0:
					border.append(node)

			print('Calcolo delle distanze rispetto i nodi del border ...')
			# trovo il nodo più vicino
			nearest_n = utils.get_nearest_node(border, minimum_length)
			solution.append(nearest_n)
			nodes_in_solution.append(nearest_n)
			minimum_length = None
			# carico il furgone della quantità del nodo corrente, se possibile
			if (load + AppData.current_node.q_p) <= AppData.capacity:
				load += AppData.current_node.q_p
				AppData.nodes[AppData.current_node.id].q_p = 0

			print('Nodo corrente:' + str(AppData.current_node))
			print('Quantità nel furgone, al primo carico dopo il nodo 0:' + str(load))

			border.clear()

			# Other steps
			while utils.complete_deliveries(total_deliveries):
				step += 1
				print('\nStep ' + str(step))

				print("-----------------nodes-------------------")
				for node in AppData.nodes:
					print(node)
				print("-------------initial_node----------------")
				for node in AppData.initial_nodes:
					print(node)
				print("-----------------------------------------")

				for node in AppData.nodes:
					if node.id != 0 and node.id != AppData.current_node.id and utils.abmissibility_greedy(node, load, nodes_in_solution):
						border.append(node)

				# to avoid deadlock
				if not border:
					for node in AppData.nodes:
						if node.id != AppData.current_node.id and node.q_p != 0:
							border.append(node)

				print('Nodi frontiera, con i vincoli imposti:')
				for node in border:
					print(node)

				print('Calcolo delle distanze rispetto i nodi di border ...')
				# trovo il nodo più vicino
				nearest_n = utils.get_nearest_node(border, minimum_length)
				solution.append(nearest_n)
				if nearest_n not in nodes_in_solution:
					nodes_in_solution.append(nearest_n)
				minimum_length = None
				print("nodo più vicino, scelto: "  + str(nearest_n))

				epsilon = 0
				# scarico il furgone della quantità del nodo corrente, se deve ricevere dal nodo corrente
				print("\nFASE DI SCARICO")
				scaricato = False
				for s in nodes_in_solution:
					for t in AppData.transfers:
						if (t.id_d == AppData.current_node.id) and (t.delivered is False) and (t.id_p == s.id):
							# print("id nodeo di pickup t.id_p = " + str(t.id_p))
							# print("initial_node_q_p= " + str(AppData.initial_nodes[t.id_p].q_p))
							# print("node_q_p= " + str(AppData.nodes[t.id_p].q_p))
							epsilon = AppData.initial_nodes[t.id_p].q_p - AppData.nodes[t.id_p].q_p
							if epsilon >= t.q:
								# print("epsilon = " + str(epsilon) + " t.q = " + str(t.q))
								load = load - t.q
								AppData.nodes[AppData.current_node.id].q_d -= t.q
								AppData.initial_nodes[t.id_p].q_p -= t.q
								print("Quantità scaricata = ", t.q)
								t.q = 0
								t.delivered = True
								total_deliveries += 1
							else:  # if epsilon < t.q
								# print("epsilon = " + str(epsilon) + "t.q = " + str(t.q))
								load = load - epsilon
								AppData.nodes[AppData.current_node.id].q_d -= epsilon
								AppData.initial_nodes[t.id_p].q_p -= epsilon
								t.q -= epsilon
								print("Quantità scaricata = ", epsilon)
							scaricato = True

				if not scaricato:
					print("Quantità scaricata = 0")

				# carico il furgone della quantità del nodo corrente, se possibile
				print("FASE DI CARICO")
				load += AppData.current_node.q_p
				if load <= AppData.capacity:
					AppData.nodes[AppData.current_node.id].q_p = 0
				else:
					scarto = load - AppData.capacity
					load = load - scarto
					AppData.nodes[AppData.current_node.id].q_p = scarto
				print("Quantità caricata = ", load)

				#print('Nodo corrente, prima di ripetere il while:' + str(AppData.current_node))
				print('\nQuantità nel furgone:' + str(load))

				print("Stato consegne")
				for t in AppData.transfers:
					print(t)

				# pulizia del bordo altrimenti rimangono altri nodi come minimo
				border.clear()

			# ritorno al deposito
			solution.append(AppData.nodes[0])
			# risultato soluzione
			print('\nDistanza totale = ' + str(AppData.total_length))
			print('Nodi nella soluzione:')
			for node in solution:
				print(node)
			# reset risultato
			AppData.total_length = 0

		if choice == "":
			pass

		if choice == "":
			pass

		if choice == "":
			pass
