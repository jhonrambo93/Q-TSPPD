from service.AppData import AppData
from node.Node import Node
from step.Step import Step
import random
import utils
import copy


class MenuHandler:

	def serve(self, choice: str) -> None:

		if choice == "GREEDY":

			# initialization
			steps = [] # id, node_previous, node_next, border, transfers, load
			step = 0
			border = []  # possibili nodi raggiungibili
			solution = []  # elenco dei nodi che compongono la soluzione, cioè il viaggio del furgoncino
			total_deliveries = 0  # totale consegne portate a termine
			load = 0  # carico nel furgone
			# unload = bool  # serve per stampare a video scaricato
			minimum_length = None
			max_value = None
			AppData.initial_nodes = copy.deepcopy(AppData.nodes)  # copio la lista nodes in initial_nodes


			# Start Greedy
			# Step 0
			AppData.current_node = AppData.nodes[0]  # impongo che il nodo iniziale è il nodo 0
			solution.append(AppData.current_node)

			for node in AppData.nodes:
				if node.q_p != 0:
					border.append(node)

			# Step 1
			step += 1
			print('\nStep ' + str(step))

			print('Calcolo delle distanze rispetto i nodi del border ...')
			# trovo il nodo più vicino
			nearest_n = utils.get_nearest_node(border, minimum_length)
			solution.append(nearest_n)
			AppData.nodes_in_solution.append(nearest_n)

			###################### Salvo ciò che viene fatto allo step 0 ##########################################
			steps.append(Step(0, AppData.current_node, None, nearest_n, copy.deepcopy(border), list(), 0, 0))
			#######################################################################################################

			#aggiono il nodo corrente, corrispondente allo step 1
			AppData.current_node = nearest_n

			minimum_length = None
			# carico il furgone della quantità del nodo corrente, se possibile
			if (load + AppData.current_node.q_p) <= AppData.capacity:
				load += AppData.current_node.q_p
				AppData.nodes[AppData.current_node.id].q_p = 0
				AppData.nodes[AppData.current_node.id].furgone = load
			else:
				print('Errore nel file transfers, il nodo ' + str(AppData.current_node.id) + ' ha q_p > ', str(AppData.capacity))
				exit()

			print('Nodo corrente:' + str(AppData.current_node))
			print('Quantità nel furgone, al primo carico dopo il nodo 0: ' + str(load))

			border.clear()

			# Salvo ciò che viene fatto allo step 1
			# id - corrente - nodo_prima - nodo_next - border - transfers - load
			steps.append(Step(1, AppData.current_node, steps[0].current_node, None, list(), list(), load, load))


			# Other steps
			while utils.complete_deliveries(total_deliveries):
				step += 1
				print('\nStep ' + str(step))

				print('-----------------nodes-------------------')
				for node in AppData.nodes:
					print(node)
				print('-------------initial_node----------------')
				for node in AppData.initial_nodes:
					print(node)
				print('-----------------------------------------')

				for node in AppData.nodes:
					if node.id != 0 and node.id != AppData.current_node.id and utils.abmissibility_greedy(node, load, AppData.nodes_in_solution):
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
				if nearest_n not in AppData.nodes_in_solution:
					AppData.nodes_in_solution.append(nearest_n)

				############Aggiorno border e nearest node dello step 1################
				steps[step-1].border = copy.deepcopy(border)
				steps[step-1].node_next = nearest_n
				#######################################################################

				AppData.current_node = nearest_n

				##########################step 2 primo aggiornamento##########################################
				# id - corrente - nodo_prima - nodo_next - border - transfers - load
				steps.append(Step(step, AppData.current_node, steps[step-1].current_node, None, list(), list(), load, 0))
				##############################################################################################
				minimum_length = None
				print('nodo più vicino, scelto: ' + str(nearest_n))

				epsilon = 0
				# scarico il furgone della quantità del nodo corrente, se deve ricevere dal nodo corrente
				print('\nFASE DI SCARICO')
				unload = False
				for s in AppData.nodes_in_solution:
					for t in AppData.transfers:
						if (t.id_d == AppData.current_node.id) and (t.delivered is False) and (t.id_p == s.id):
							# print("id nodeo di pickup t.id_p = " + str(t.id_p))
							# print("initial_node_q_p= " + str(AppData.initial_nodes[t.id_p].q_p))
							# print("node_q_p= " + str(AppData.nodes[t.id_p].q_p))
							epsilon = AppData.initial_nodes[t.id_p].q_p - AppData.nodes[t.id_p].q_p
							if epsilon >= t.q:
								# print("epsilon = " + str(epsilon) + " t.q = " + str(t.q))
								load = load - t.q
								AppData.nodes[t.id_p].furgone -= t.q
								AppData.nodes[AppData.current_node.id].q_d -= t.q
								AppData.initial_nodes[t.id_p].q_p -= t.q
								print('Quantità scaricata = ', t.q)

								t.delivered = True
								################################
								steps[step].transfers.append(t)
								################################
								t.q = 0
								total_deliveries += 1


							else:  # if epsilon < t.q
								# print("epsilon = " + str(epsilon) + "t.q = " + str(t.q))
								load = load - epsilon
								AppData.nodes[t.id_p].furgone -= epsilon
								AppData.nodes[AppData.current_node.id].q_d -= epsilon
								AppData.initial_nodes[t.id_p].q_p -= epsilon
								#################################
								steps[step].transfers.append(t)
								#################################
								t.q -= epsilon
								print('Quantità scaricata = ', epsilon)

							unload = True

				if not unload:
					print('Quantità scaricata = 0')

				print('\nQuantità nel furgone:' + str(load))
				# carico il furgone della quantità del nodo corrente, se possibile
				print('FASE DI CARICO')
				load += AppData.current_node.q_p
				if load <= AppData.capacity:
					print('Quantità caricata = ', AppData.nodes[AppData.current_node.id].q_p)
					###############################################################################
					steps[step].carico = AppData.nodes[AppData.current_node.id].q_p
					###############################################################################
					AppData.nodes[AppData.current_node.id].furgone += AppData.nodes[AppData.current_node.id].q_p
					AppData.nodes[AppData.current_node.id].q_p = 0
				elif load > AppData.capacity:
					scarto = load - AppData.capacity
					load = load - scarto
					carico = AppData.nodes[AppData.current_node.id].furgone = AppData.nodes[AppData.current_node.id].furgone + (AppData.nodes[AppData.current_node.id].q_p - scarto)
					AppData.nodes[AppData.current_node.id].q_p = scarto
					print('Quantità caricataa = ', carico)
					###############################################
					steps[step].carico = carico
					###############################################

				# print('Nodo corrente, prima di ripetere il while:' + str(AppData.current_node))
				print('\nQuantità nel furgone:' + str(load))

				##################################
				steps[step].load = load
				##################################

				print('Stato consegne')
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
			total_deliveries = 0

		if choice == "DESTROY AND REPAIR":
			j = random.randint(2,step-1) #lo step finale con 0 non c'è quindi step-1 per non andare in overflow
			if steps[j].carico == 0 and utils.is_next_present(steps, j):
				#print('Il nodo ' + str(steps[j].current_node.id) + ' allo step' + str(j) + ' può essere eliminato')

				#possiamo eliminare lo step[j]
				#mettere volanti i task (trasferimenti)
				#aggiornare il furgone

			else:
				print('Non è possibile effettuare miglioramenti alla soluzione')





		if choice == "GREEDY_BY_VALUE":
			# initialization
			step = 0
			border = []  # possibili nodi raggiungibili
			solution = []  # elenco dei nodi che compongono la soluzione, cioè il viaggio del furgoncino
			total_deliveries = 0  # totale consegne portate a termine
			load = 0  # carico nel furgone
			# unload = bool  # serve per stampare a video scaricato
			max_value = None
			AppData.initial_nodes = copy.deepcopy(AppData.nodes)  # copio la lista nodes in initial_nodes

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
			# trovo il nodo migliore
			best_n = utils.get_best_node(border, max_value, load)
			solution.append(best_n)
			AppData.nodes_in_solution.append(best_n)
			max_value = None
			# carico il furgone della quantità del nodo corrente, se possibile
			if (load + AppData.current_node.q_p) <= AppData.capacity:
				load += AppData.current_node.q_p
				AppData.nodes[AppData.current_node.id].q_p = 0
				AppData.nodes[AppData.current_node.id].furgone = load

			print('Nodo corrente:' + str(AppData.current_node))
			print('Quantità nel furgone, al primo carico dopo il nodo 0:' + str(load))

			border.clear()

			# Other steps
			while utils.complete_deliveries(total_deliveries):
				step += 1
				print('\nStep ' + str(step))

				print('-----------------nodes-------------------')
				for node in AppData.nodes:
					print(node)
				print('-------------initial_node----------------')
				for node in AppData.initial_nodes:
					print(node)
				print('-----------------------------------------')

				for node in AppData.nodes:
					if node.id != 0 and node.id != AppData.current_node.id and utils.abmissibility_greedy(node, load, AppData.nodes_in_solution):
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
				best_n = utils.get_best_node(border, max_value, load)
				solution.append(best_n)
				AppData.nodes_in_solution.append(best_n)
				if best_n not in AppData.nodes_in_solution:
					AppData.nodes_in_solution.append(best_n)
				minimum_length = None
				print('nodo più vicino, scelto: ' + str(best_n))

				epsilon = 0
				# scarico il furgone della quantità del nodo corrente, se deve ricevere dal nodo corrente
				print('\nFASE DI SCARICO')
				unload = False
				for s in AppData.nodes_in_solution:
					for t in AppData.transfers:
						if (t.id_d == AppData.current_node.id) and (t.delivered is False) and (t.id_p == s.id):
							# print("id nodeo di pickup t.id_p = " + str(t.id_p))
							# print("initial_node_q_p= " + str(AppData.initial_nodes[t.id_p].q_p))
							# print("node_q_p= " + str(AppData.nodes[t.id_p].q_p))
							epsilon = AppData.initial_nodes[t.id_p].q_p - AppData.nodes[t.id_p].q_p
							if epsilon >= t.q:
								# print("epsilon = " + str(epsilon) + " t.q = " + str(t.q))
								load = load - t.q
								AppData.nodes[t.id_p].furgone -= t.q
								AppData.nodes[AppData.current_node.id].q_d -= t.q
								AppData.initial_nodes[t.id_p].q_p -= t.q
								print('Quantità scaricata = ', t.q)
								t.q = 0
								t.delivered = True
								total_deliveries += 1
							else:  # if epsilon < t.q
								# print("epsilon = " + str(epsilon) + "t.q = " + str(t.q))
								load = load - epsilon
								AppData.nodes[t.id_p].furgone -= epsilon
								AppData.nodes[AppData.current_node.id].q_d -= epsilon
								AppData.initial_nodes[t.id_p].q_p -= epsilon
								t.q -= epsilon
								print('Quantità scaricata = ', epsilon)
							unload = True

				if not unload:
					print('Quantità scaricata = 0')

				print('\nQuantità nel furgone:' + str(load))
				# carico il furgone della quantità del nodo corrente, se possibile
				print('FASE DI CARICO')
				load += AppData.current_node.q_p
				if load <= AppData.capacity:
					print('Quantità caricata = ', AppData.nodes[AppData.current_node.id].q_p)
					AppData.nodes[AppData.current_node.id].furgone += AppData.nodes[AppData.current_node.id].q_p
					AppData.nodes[AppData.current_node.id].q_p = 0
				elif load > AppData.capacity:
					scarto = load - AppData.capacity
					load = load - scarto
					carico = AppData.nodes[AppData.current_node.id].furgone = AppData.nodes[
																				  AppData.current_node.id].furgone + (
																						  AppData.nodes[
																							  AppData.current_node.id].q_p - scarto)
					AppData.nodes[AppData.current_node.id].q_p = scarto
					print('Quantità caricataaaaaaa = ', carico)

				# print('Nodo corrente, prima di ripetere il while:' + str(AppData.current_node))
				print('\nQuantità nel furgone:' + str(load))

				print('Stato consegne')
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
