from service.AppData import AppData
from node.Node import Node
import utils


class MenuHandler:

	def serve(self, choice: str) -> None:
		""" Handle the peer packet

		:param choice: the choice to handle
		:return: None
		"""

		if choice == "GREEDY":
			# init
			step = 0
			border = []
			solution = []
			nodes_in_solution = []
			total_deliveries = 0
			AppData.current_node = AppData.nodes[0]
			solution.append(AppData.current_node)
			minimum_length = None
			load = 0  # carico nel furgone

			# first step
			for node in AppData.nodes:
				if node.q_p != 0:
					border.append(node)

			for node in border:
				print(node)

			print('Distanze nodi frontiera dal nodo 0:')
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
				print('Step ' + str(step))
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

				print('Distanze nodi frontiera dal nodo corrente:')
				# trovo il nodo più vicino
				nearest_n = utils.get_nearest_node(border, minimum_length)
				solution.append(nearest_n)
				if nearest_n not in nodes_in_solution:
					nodes_in_solution.append(nearest_n)
				minimum_length = None
				print("nodo più vicino scelto:" + str(nearest_n))
				print('Nodi prima di modifica di q:')
				for node in AppData.nodes:
					print(node)

				# scarico il furgone della quantità del nodo corrente, se deve ricevere dal nodo corrente
				for s in nodes_in_solution:
					for t in AppData.transfers:
						if (t.id_d == AppData.current_node.id) and (t.delivered is False) and (t.id_p == s.id):
							load = load - t.q  # scarico il furgone della quantità
							# decremento della quantità t.q nella lista dei nodi
							AppData.nodes[AppData.current_node.id].q_d = AppData.nodes[AppData.current_node.id].q_d - t.q
							t.q = 0
							t.delivered = True
							total_deliveries = total_deliveries + 1

				# carico il furgone della quantità del nodo corrente, se possibile

				load += AppData.current_node.q_p
				if load <= AppData.capacity:
					AppData.nodes[AppData.current_node.id].q_p = 0
				else:
					scarto = load - AppData.capacity
					load = load - scarto
					AppData.nodes[AppData.current_node.id].q_p = scarto

				print('Nodo corrente, prima di ripetere il while:' + str(AppData.current_node))
				print('Quantità nel furgone:' + str(load))

				# pulizia del bordo altrimenti rimangono altri nodi come minimo
				border.clear()

			# ritorno al deposito
			solution.append(AppData.nodes[0])
			# risultato soluzione
			print('Distanza totale:' + str(AppData.total_length))
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
