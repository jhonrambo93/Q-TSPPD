from service.AppData import AppData
from node.Node import Node
import math


def lenght(node_1: Node, node_2: Node):
    return math.sqrt((node_1.x - node_2.x) ** 2 + (node_1.y - node_2.y) ** 2)


class MenuHandler:

	def serve(self, choice: str) -> None:
		""" Handle the peer packet

		:param choice: the choice to handle
		:return: None
		"""

		if choice == "GREEDY":
			# start
			n_c = AppData.nodes[0] # nodo corrente che inizialmente è il nodo 0
			border = []
			solution = []
			solution.append(n_c)
			min_l = None
			min_n = None
			q = 0 # quantità nel furgone
			for node in AppData.nodes:
				if node.q_p != 0:
					border.append(node)
			# for della GREEDY
			for n_f in border:
				l = lenght(n_c, n_f)
				print(l)
				if min_l is None:
					min_l = l
					min_n = n_f
				elif l < min_l:
					min_l = l
					min_n = n_f
			solution.append(min_n)
			n_c = min_n
			# Corico e scarico Nodo corrente
			print('Nodo corrente, appena preso in carico,')
			print(n_c)

			# scarico il furgone della quantità del nodo corrente, se deve ricevere dal nodo corrente

			for t in AppData.transfers:
				if (t.id_d == n_c.id) and (t.delivered == False):
					pass
					# if t.id_p è nella lista dei nodi da cui ho prelevato
					# allora q = q - t_q , t.q = 0 e t.delivered = True

			for node in solution:
				if (n_c.q_d != 0):
					q = q - n_c.q_d # sarebbe q = q + n_c.q_p, l'ho scritto il modo più sintetico
					AppData.nodes[n_c.id].q_d = AppData.nodes[n_c.id].q_d - q

			# carico il furgone della quantità del nodo corrente, se possibile
			if (q+n_c.q_p) < AppData.Q:
				q += n_c.q_p
				AppData.nodes[n_c.id].q_p = 0
			print('Nodo corrente, dopo aver prelevato q_p')
			print(n_c)
			print('Quantità nel furgone')
			print(q)


		if choice == "":
			pass

		if choice == "":
			pass

		if choice == "":
			pass