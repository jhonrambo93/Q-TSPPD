from service.AppData import AppData
from node.Node import Node
import math


def lenght(node_1: Node, node_2: Node) -> float:
    return math.sqrt((node_1.x - node_2.x) ** 2 + (node_1.y - node_2.y) ** 2)


# Funzione ammissibilità nodo successivo
def abmissibility_greedy(node: Node, q: int, nodes_in_solution: list) -> bool:
	if node.q_p == 0 and node.q_d == 0:
		return False
	else:
		# Se metto < invece di <= siamo nel caso in cui il bordo non viene creato, risolvere il problema!???
		if is_destination(node, nodes_in_solution) and q-AppData.q_d_n+node.q_p <= AppData.Q:
			return True
		else:
			return False


def is_destination(node: Node, nodes_in_solution: list) -> bool:
	AppData.q_d_n = 0
	for n_s in nodes_in_solution:
		for t in AppData.transfers:
			if t.delivered is False and n_s.id == t.id_p:
				if t.id_d == node.id:
					AppData.q_d_n = t.q # Quantità corretta da scaricare
					return True
	return False


def end_greedy() -> bool:
	complete_deliver = 0
	for transfer in AppData.transfers:
		if transfer.delivered is True:
			complete_deliver = complete_deliver + 1
	if len(AppData.transfers) == complete_deliver:
		return False
	else:
		return True


class MenuHandler:

	def serve(self, choice: str) -> None:
		""" Handle the peer packet

		:param choice: the choice to handle
		:return: None
		"""

		if choice == "GREEDY":
			# init
			n_c = AppData.nodes[0]  # nodo corrente che inizialmente è il nodo 0
			border = []
			solution = []
			nodes_in_solution = []
			solution.append(n_c)
			min_l = None
			nearest_n = None
			q = 0  # quantità nel furgone

			# first step
			for node in AppData.nodes:
				if node.q_p != 0:
					border.append(node)
			print("stampo lunghezze tra i nodi dal nodo corrente")
			for n_f in border:
				l = lenght(n_c, n_f)
				print(l)
				if min_l is None:
					min_l = l
					nearest_n = n_f
				elif l < min_l:
					min_l = l
					nearest_n = n_f
			solution.append(nearest_n)
			n_c = nearest_n
			min_l = None
			nodes_in_solution.append(nearest_n)
			# carico il furgone della quantità del nodo corrente, se possibile
			if (q + n_c.q_p) < AppData.Q:
				q += n_c.q_p
				AppData.nodes[n_c.id].q_p = 0
			print('Quantità nel furgone, al primo carico dopo il nodo 0')
			print(q)

			border.clear()

			# Other steps
			while end_greedy():

				for node in AppData.nodes:
					if node.id != 0 and node.id != n_c.id and abmissibility_greedy(node, q, nodes_in_solution):
						border.append(node)

				if not border:
					for node in AppData.nodes:
						if node.id != n_c.id and node.q_p != 0:
							border.append(node)

				print("stampo nodi nel bordo con i vari vincoli imposti:")

				for node in border:
					print(node)

				print("stampo lunghezze tra i nodi dal nodo corrente")
				for n_f in border:
					if n_f.id != n_c.id:
						l = lenght(n_c, n_f)
						print(l)
						if min_l is None:
							min_l = l
							nearest_n = n_f
						elif l < min_l:
							min_l = l
							nearest_n = n_f
				solution.append(nearest_n)
				n_c = nearest_n
				if nearest_n not in nodes_in_solution:
					nodes_in_solution.append(nearest_n)
				min_l = None
				# print("nodo più vicino scelto:")
				# print(nearest_n)
				print("altra print nodi prima di modifica di q")
				for node in AppData.nodes:
					print(node)

				# scarico il furgone della quantità del nodo corrente, se deve ricevere dal nodo corrente
				for s in solution:
					for t in AppData.transfers:
						if (t.id_d == n_c.id) and (t.delivered is False) and (t.id_p == s.id):
							q = q - t.q  # scarico il furgone della quantità
							AppData.nodes[n_c.id].q_d = AppData.nodes[n_c.id].q_d - t.q  # decremento della quantità t.q nella lista dei nodi
							t.q = 0
							t.delivered = True

				# carico il furgone della quantità del nodo corrente, se possibile
				q += n_c.q_p
				AppData.nodes[n_c.id].q_p = 0

				print('Nodo corrente, prima di ripetere il while')
				print(n_c)
				print('Quantità nel furgone')
				print(q)

				print("pulizia del bordo altrimenti rimangono altri nodi come minimo")
				border.clear()

			# ritorno al deposito
			solution.append(AppData.nodes[0])

			print("Nodi nella soluzione:")
			for node in solution:
				print(node)

		if choice == "":
			pass

		if choice == "":
			pass

		if choice == "":
			pass
