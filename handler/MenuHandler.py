from service.AppData import AppData
from node.Node import Node
import math


def lenght(node_1: Node, node_2: Node) -> float:
    return math.sqrt((node_1.x - node_2.x) ** 2 + (node_1.y - node_2.y) ** 2)


def abmissibility_greedy(node: Node, q: int, transfer: list, solution: list) -> bool:
	if node.q_p != 0 and node.q_d != 0:
		if istot(node, transfer, solution) and q-node.q_d+node.q_p < AppData.Q:
			return True
	return False


def istot(node: Node, transfer: list, solution: list) -> bool:
	for t in transfer:
		for n_s in solution:
			if n_s.id == t.id_p:
				if t.id_d == node.id:
					return True
				return False


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
			solution.append(n_c)
			min_l = None
			min_n = None
			q = 0  # quantità nel furgone

			# first step
			for node in AppData.nodes:
				if node.q_p != 0:
					border.append(node)
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

			# carico il furgone della quantità del nodo corrente, se possibile
			if (q + n_c.q_p) < AppData.Q:
				q += n_c.q_p
				AppData.nodes[n_c.id].q_p = 0

			# other steps
			while True:

				for node in AppData.nodes:
					if abmissibility_greedy(node, q, AppData.transfers, solution):
						border.append(node)
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

				# scarico il furgone della quantità del nodo corrente, se deve ricevere dal nodo corrente
				for t in AppData.transfers:
					if (t.id_d == n_c.id) and (t.delivered is False):
						q = q - t.q
						t.q = 0
						t.delivered = True
				# da riguardare!!!
				for node in AppData.nodes:
					if n_c.q_d != 0:
						q = q - n_c.q_d  # sarebbe q = q + n_c.q_p, l'ho scritto il modo più sintetico
						node.q_d = node.q_d - q

				# carico il furgone della quantità del nodo corrente, se possibile
				# if (q+n_c.q_p) < AppData.Q:
				q += n_c.q_p
				AppData.nodes[n_c.id].q_p = 0

				print('Nodo corrente, dopo aver prelevato q_p')
				print(n_c)
				print('Quantità nel furgone')
				print(q)

			# ritorno al deposito
			solution.append(AppData.nodes[0])

		if choice == "":
			pass

		if choice == "":
			pass

		if choice == "":
			pass