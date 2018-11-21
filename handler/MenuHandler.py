from service.AppData import AppData
from node.Node import Node
from step.Step import Step
import random
import utils
import copy


class MenuHandler:

	def serve(self, choice: str) -> None:

		if choice == "GREEDY":

			# init
			AppData.total_length = 0
			step = 0
			border = []  # possibili nodi raggiungibili
			solution = []  # elenco dei nodi che compongono la soluzione, cioè il viaggio del furgoncino
			total_deliveries = 0  # totale consegne portate a termine
			load = 0  # carico nel furgone
			minimum_length = None
			AppData.initial_nodes = copy.deepcopy(AppData.nodes)  # copio la lista nodes in initial_nodes

			# Start Greedy
			# Step 0
			AppData.current_node = AppData.nodes[0]  # impongo che il nodo iniziale è il nodo 0
			solution.append(AppData.current_node)
			# Generarione Immagine della soluzione parziale
			# utils.images_sol_generation(solution)

			for node in AppData.nodes:
				if node.q_p != 0:
					border.append(node)

			# Step 1
			step += 1
			print('\nStep: ' + str(step))

			print('Calcolo delle distanze rispetto i nodi del border ... ')

			# trovo il nodo più vicino
			nearest_n = utils.get_nearest_node(border, minimum_length)
			solution.append(nearest_n)
			AppData.nodes_in_solution.append(nearest_n)
			# Generarione Immagine della soluzione parziale
			# utils.images_sol_generation(solution)

			# ############################# Salvo ciò che viene fatto allo step 0 #####################################
			AppData.steps.append(Step(0, AppData.current_node, None, nearest_n, copy.deepcopy(border), list(), 0, 0, 1))
			# #########################################################################################################

			# aggiorno il nodo corrente, corrispondente allo step 1
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
			print('Quantità nel furgone: ' + str(load))

			border.clear()

			# ##################################Salvo ciò che viene fatto allo step 1##################################
			AppData.steps.append(Step(1, AppData.current_node, AppData.steps[0].current_node, None, list(), list(), load, load, 1))
			# #########################################################################################################

			# Other steps
			while utils.complete_deliveries(total_deliveries):
				step += 1
				print('\nStep: ' + str(step))

				for node in AppData.nodes:
					if node.id != 0 and node.id != AppData.current_node.id and utils.abmissibility_greedy(node, AppData.nodes_in_solution):
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
				# Generarione Immagine della soluzione parziale
				# utils.images_sol_generation(solution)

				# ###########Aggiorno border e nearest node dello step 1###############################################
				AppData.steps[step-1].border = copy.deepcopy(border)
				AppData.steps[step-1].node_next = nearest_n
				# #####################################################################################################

				AppData.current_node = nearest_n

				# #########################step 2 primo aggiornamento##########################################
				AppData.steps.append(Step(step, AppData.current_node, AppData.steps[step-1].current_node, None, list(), list(), load, 0, 1))
				# #############################################################################################

				minimum_length = None
				print('Nodo scelto: ' + str(nearest_n))

				# scarico il furgone della quantità del nodo corrente, se deve ricevere dal nodo corrente
				print('\nFASE DI SCARICO')
				unload = False
				for s in AppData.nodes_in_solution:
					for t in AppData.transfers:
						if (t.id_d == AppData.current_node.id) and (t.delivered is False) and (t.id_p == s.id):
							epsilon = AppData.initial_nodes[t.id_p].q_p - AppData.nodes[t.id_p].q_p
							if epsilon >= t.q:
								load = load - t.q
								AppData.nodes[t.id_p].furgone -= t.q
								AppData.nodes[AppData.current_node.id].q_d -= t.q
								AppData.initial_nodes[t.id_p].q_p -= t.q
								print('Quantità scaricata = ', t.q)

								t.delivered = True
								# ##########################################
								AppData.steps[step].transfers.append(copy.deepcopy(t))
								# ##########################################
								t.q = 0
								total_deliveries += 1

							else:  # if epsilon < t.q
								load = load - epsilon
								AppData.nodes[t.id_p].furgone -= epsilon
								AppData.nodes[AppData.current_node.id].q_d -= epsilon
								AppData.initial_nodes[t.id_p].q_p -= epsilon
								t.q -= epsilon
								# ####################################################################
								# metto il task in coda ai task dello step
								AppData.steps[step].transfers.append(copy.deepcopy(t))
								# al task corrente vado a mettergli il corretto q rimasto
								AppData.steps[step].transfers[len(AppData.steps[step].transfers) - 1].q = epsilon
								# ####################################################################

								print('Quantità scaricata = ', epsilon)

							unload = True

				if not unload:
					print('Quantità scaricata = 0')

				# carico il furgone della quantità del nodo corrente, se possibile
				print('FASE DI CARICO')
				load += AppData.current_node.q_p
				if load <= AppData.capacity:
					print('Quantità caricata = ', AppData.nodes[AppData.current_node.id].q_p)
					# ##############################################################################
					AppData.steps[step].carico = AppData.nodes[AppData.current_node.id].q_p
					# ##############################################################################
					AppData.nodes[AppData.current_node.id].furgone += AppData.nodes[AppData.current_node.id].q_p
					AppData.nodes[AppData.current_node.id].q_p = 0
				elif load > AppData.capacity:
					scarto = load - AppData.capacity
					load = load - scarto
					carico = AppData.nodes[AppData.current_node.id].furgone = AppData.nodes[AppData.current_node.id].furgone + (AppData.nodes[AppData.current_node.id].q_p - scarto)
					AppData.nodes[AppData.current_node.id].q_p = scarto
					print('Quantità caricata = ', carico)
					# ##############################################
					AppData.steps[step].carico = carico
					# ##############################################

				print('\nQuantità nel furgone:' + str(load))

				# #################################
				AppData.steps[step].load = load
				# #################################

				print('Stato consegne: ')
				for t in AppData.transfers:
					print(t)

				# pulizia del bordo
				border.clear()

			# ritorno al deposito
			solution.append(AppData.nodes[0])
			# risultato soluzione
			print('SOLUZIONE: ')
			print('\nDistanza totale = ' + str(AppData.total_length))
			print('Sequenza nodi soluzione:')
			for node in solution:
				print(node)

			# ###########Aggiorno next node del penultimo step (prima del ritorno al deposito)################
			AppData.steps[step].node_next = solution[0]
			# ################################################################################################

			# Inserisco gli step della soluzione della greedy come primo elemento nella set_solutione
			# e relativa lunghezza in len_set_solution
			AppData.set_solution.append(AppData.steps)
			AppData.len_set_solution.append(AppData.total_length)

			# ***************** Generarione Immagine della soluzione definitiva *******************
			utils.images_sol_generation(solution)
			# *************************************************************************************


		if choice == "GREEDY_RANDOM":
			# initialization
			AppData.total_length = 0
			step = 0
			border = []  # possibili nodi raggiungibili
			solution = []  # elenco dei nodi che compongono la soluzione, cioè il viaggio del furgoncino
			total_deliveries = 0  # totale consegne portate a termine
			load = 0  # carico nel furgone
			# unload = bool  # serve per stampare a video scaricato
			minimum_length = None
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

			# scelgo un nodo random

			j = random.randint(0, (len(border) - 1))
			nearest_n = border[j]
			AppData.total_length += utils.lenght(AppData.current_node, border[j])
			solution.append(nearest_n)
			AppData.nodes_in_solution.append(nearest_n)

			# ##################### Salvo ciò che viene fatto allo step 0 ##########################################
			AppData.steps.append(Step(0, AppData.current_node, None, nearest_n, copy.deepcopy(border), list(), 0, 0, 1))
			# ######################################################################################################

			# aggiono il nodo corrente, corrispondente allo step 1
			AppData.current_node = nearest_n

			minimum_length = None
			# carico il furgone della quantità del nodo corrente, se possibile
			if (load + AppData.current_node.q_p) <= AppData.capacity:
				load += AppData.current_node.q_p
				AppData.nodes[AppData.current_node.id].q_p = 0
				AppData.nodes[AppData.current_node.id].furgone = load
			else:
				print('Errore nel file transfers, il nodo ' + str(AppData.current_node.id) + ' ha q_p > ',
					  str(AppData.capacity))
				exit()

			print('Nodo corrente:' + str(AppData.current_node))
			print('Quantità nel furgone, al primo carico dopo il nodo 0: ' + str(load))

			border.clear()

			# Salvo ciò che viene fatto allo step 1
			# id - corrente - nodo_prima - nodo_next - border - transfers - load
			AppData.steps.append(
				Step(1, AppData.current_node, AppData.steps[0].current_node, None, list(), list(), load, load, 1))

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
					if node.id != 0 and node.id != AppData.current_node.id and utils.abmissibility_greedy(node, AppData.nodes_in_solution):
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
				# nodo random
				j = random.randint(0, (len(border) - 1))
				nearest_n = border[j]
				AppData.total_length += utils.lenght(AppData.current_node, border[j])
				solution.append(nearest_n)
				if nearest_n not in AppData.nodes_in_solution:
					AppData.nodes_in_solution.append(nearest_n)

				# ###########Aggiorno border e nearest node dello step 1################
				AppData.steps[step - 1].border = copy.deepcopy(border)
				AppData.steps[step - 1].node_next = nearest_n
				# ######################################################################

				AppData.current_node = nearest_n

				# #########################step 2 primo aggiornamento##########################################
				# id - corrente - nodo_prima - nodo_next - border - transfers - load
				AppData.steps.append(Step(step, AppData.current_node, AppData.steps[step - 1].current_node, None, list(), list(), load, 0, 1))
				# #############################################################################################
				minimum_length = None
				print('nodo più vicino, scelto: ' + str(nearest_n))

				# epsilon = 0
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
								# ##########################################
								AppData.steps[step].transfers.append(copy.deepcopy(t))
								# ##########################################
								t.q = 0
								total_deliveries += 1

							else:  # if epsilon < t.q
								# print("epsilon = " + str(epsilon) + "t.q = " + str(t.q))
								load = load - epsilon
								AppData.nodes[t.id_p].furgone -= epsilon
								AppData.nodes[AppData.current_node.id].q_d -= epsilon
								AppData.initial_nodes[t.id_p].q_p -= epsilon
								t.q -= epsilon
								# ####################################################################
								AppData.steps[step].transfers.append(
									copy.deepcopy(t))  # metto il task in coda ai task dello step
								# len(AppData.steps[step].transfers): quanti task ho nello step
								# al task corrente vado a mettergli il corretto q rimasto
								AppData.steps[step].transfers[len(AppData.steps[step].transfers) - 1].q = epsilon
								# ####################################################################
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
					# ##############################################################################
					AppData.steps[step].carico = AppData.nodes[AppData.current_node.id].q_p
					# ##############################################################################
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
					print('Quantità caricata = ', carico)
					# ##############################################
					AppData.steps[step].carico = carico
				# ##############################################

				# print('Nodo corrente, prima di ripetere il while:' + str(AppData.current_node))
				print('\nQuantità nel furgone:' + str(load))

				# #################################
				AppData.steps[step].load = load
				# #################################

				print('Stato consegne')
				for t in AppData.transfers:
					print(t)

				# pulizia del bordo
				border.clear()

			# ritorno al deposito
			solution.append(AppData.nodes[0])
			# risultato soluzione
			print('\nDistanza totale = ' + str(AppData.total_length))
			print('Nodi nella soluzione:')
			for node in solution:
				print(node)

			# ###########Aggiorno next node del penultimo step (prima del ritorno al deposito)################
			AppData.steps[step].node_next = solution[0]
			# ######################################################################

			# Inserisco gli step della soluzione della greedy come primo elemento nella set_solutione
			# e relativa lunghezza in len_set_solution
			AppData.set_solution.append(AppData.steps)
			AppData.len_set_solution.append(AppData.total_length)

		if choice == "GREEDY_BY_VALUE":
			# initialization
			AppData.total_length = 0
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

			for node in AppData.nodes:
				if node.q_p != 0:
					border.append(node)

			# Step 1

			step += 1
			print('\nStep ' + str(step))

			print('Calcolo delle distanze rispetto i nodi del border ...')

			# trovo il nodo migliore con funzione 1
			# best_n = utils.get_best_node(border, max_value, load)

			# trovo il nodo migliore con la funzione 2
			best_n = utils.get_best_node_2(border, max_value, load)

			solution.append(best_n)
			AppData.nodes_in_solution.append(best_n)

			# ##################### Salvo ciò che viene fatto allo step 0 ##########################################
			AppData.steps.append(Step(0, AppData.current_node, None, best_n, copy.deepcopy(border), list(), 0, 0, 1))
			# ######################################################################################################

			# aggiono il nodo corrente, corrispondente allo step 1
			AppData.current_node = best_n

			max_value = None

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
			AppData.steps.append(Step(1, AppData.current_node, AppData.steps[0].current_node, None, list(), list(), load, load, 1))

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
					if node.id != 0 and node.id != AppData.current_node.id and utils.abmissibility_greedy(node, AppData.nodes_in_solution):
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
				# trovo il nodo migliore con la funzione 1
				# best_n = utils.get_best_node(border, max_value, load)

				# trovo il nodo migliore con la funzione 2
				best_n = utils.get_best_node_2(border, max_value, load)

				solution.append(best_n)
				AppData.nodes_in_solution.append(best_n)
				if best_n not in AppData.nodes_in_solution:
					AppData.nodes_in_solution.append(best_n)

				# ###########Aggiorno border e nearest node dello step 1################
				AppData.steps[step - 1].border = copy.deepcopy(border)
				AppData.steps[step - 1].node_next = best_n
				# ######################################################################

				AppData.current_node = best_n

				# #########################step 2 primo aggiornamento##########################################
				# id - corrente - nodo_prima - nodo_next - border - transfers - load
				AppData.steps.append(
					Step(step, AppData.current_node, AppData.steps[step - 1].current_node, None, list(), list(), load,
						 0, 1))
				# #############################################################################################
				max_value = None
				print('nodo migliore, scelto: ' + str(best_n))

				# epsilon = 0
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
								# ##########################################
								AppData.steps[step].transfers.append(copy.deepcopy(t))
								# ##########################################
								t.q = 0
								total_deliveries += 1

							else:  # if epsilon < t.q
								# print("epsilon = " + str(epsilon) + "t.q = " + str(t.q))
								load = load - epsilon
								AppData.nodes[t.id_p].furgone -= epsilon
								AppData.nodes[AppData.current_node.id].q_d -= epsilon
								AppData.initial_nodes[t.id_p].q_p -= epsilon
								t.q -= epsilon
								# ####################################################################
								AppData.steps[step].transfers.append(
									copy.deepcopy(t))  # metto il task in coda ai task dello step
								# len(AppData.steps[step].transfers): quanti task ho nello step
								# al task corrente vado a mettergli il corretto q rimasto
								AppData.steps[step].transfers[len(AppData.steps[step].transfers) - 1].q = epsilon
								# ####################################################################
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
					# ##############################################################################
					AppData.steps[step].carico = AppData.nodes[AppData.current_node.id].q_p
					# ##############################################################################
					AppData.nodes[AppData.current_node.id].furgone += AppData.nodes[AppData.current_node.id].q_p
					AppData.nodes[AppData.current_node.id].q_p = 0
				elif load > AppData.capacity:
					scarto = load - AppData.capacity
					load = load - scarto
					carico = AppData.nodes[AppData.current_node.id].furgone = AppData.nodes[AppData.current_node.id].furgone + (AppData.nodes[AppData.current_node.id].q_p - scarto)
					AppData.nodes[AppData.current_node.id].q_p = scarto
					print('Quantità caricata = ', carico)
					# ##############################################
					AppData.steps[step].carico = carico
				# ##############################################

				# print('Nodo corrente, prima di ripetere il while:' + str(AppData.current_node))
				print('\nQuantità nel furgone:' + str(load))

				# #################################
				AppData.steps[step].load = load
				# #################################

				print('Stato consegne')
				for t in AppData.transfers:
					print(t)

				# pulizia del bordo
				border.clear()

			# ritorno al deposito
			solution.append(AppData.nodes[0])
			# risultato soluzione
			print('\nDistanza totale = ' + str(AppData.total_length))
			print('Nodi nella soluzione:')
			for node in solution:
				print(node)

			# ###########Aggiorno next node del penultimo step (prima del ritorno al deposito)################
			AppData.steps[step].node_next = solution[0]
			# ######################################################################

			# Inserisco gli step della soluzione della greedy come primo elemento nella set_solutione
			# e relativa lunghezza in len_set_solution
			AppData.set_solution.append(AppData.steps)
			AppData.len_set_solution.append(AppData.total_length)

		if choice == "DESTROY_AND_REPAIR":

			x = 0  # contatore di quello
			not_delivered = 0
			fail = 0  # fail solution counter
			stop = False  # serve dopo aver trovato una nuova soluzione

			destroy_and_repair_steps = copy.deepcopy(AppData.set_solution[0])
			memory_random = copy.deepcopy(AppData.set_solution[0])  # steps per la random
			# random che mi va a scegliere uno step da distruggere
			# lo step finale prima dello 0 non ha successori quindi step-1 per non andare in overflow
			del memory_random[len(memory_random) - 1]  # tolgo l'ultimo
			del memory_random[0]  # tolgo il primo
			del memory_random[0]  # tolgo il primo della "nuova lista" che corrisponderebbe a memory_random[1]

			while fail < 3 and (len(memory_random) != 0):

				if stop:  # se stop è vero, cioè ho trovato trovato un miglioramento/peggioramento
					destroy_and_repair_steps = copy.deepcopy(AppData.set_solution[x])
					memory_random = copy.deepcopy(AppData.set_solution[x])  # steps per la random
					del memory_random[len(memory_random) - 1]  # tolgo l'ultimo
					del memory_random[0]  # tolgo il primo
					del memory_random[0]  # tolgo il primo della "nuova lista" che corrisponderebbe a memory_random[1]
					stop = False
				else:
					# fase di scelta random tra gli step possibili
					step_random = random.choice(memory_random)  # scelgo a caso un elemento dalla lista
					j = step_random.id  # j, numero intero, è lo step che vado a selezionare
					# vado ad eliminare da memory_random lo step appena scelto
					step = 0
					go = True
					while go:
						if memory_random[step].id == step_random.id:
							del memory_random[step]
							go = False
						else:
							step += 1
					if destroy_and_repair_steps[j].carico == 0 and utils.is_next_present(j) and destroy_and_repair_steps[j].node_previous.id != destroy_and_repair_steps[j].node_next.id:
						print('Step selected: ' + str(j))
						# Metto volanti i task (trasferimenti)
						for t in destroy_and_repair_steps[j].transfers:
							# li confronto con i trasferimenti iniziali
							for k in AppData.transfers:
								if t.id_p == k.id_p and t.id_d == k.id_d:
									k.delivered = False
									k.q = t.q
									not_delivered += t.q
						i = j
						n_over = 0  # step con overload
						# while che mi permette di ridistribuire i task spachettati dallo step appena distrutto
						while not_delivered != 0 and i < len(destroy_and_repair_steps) - 1:
							i += 1
							destroy_and_repair_steps[i].load += not_delivered
							# se rispetto il vincolo della capacità
							if destroy_and_repair_steps[i].load <= AppData.capacity:
								# controllo se lo step ha come nodo quello eliminato
								# i task del nodo eliminato li dobbiamo mettere nel nodo corrente
								if destroy_and_repair_steps[i].current_node.id == destroy_and_repair_steps[j].current_node.id:
									for transfer in destroy_and_repair_steps[j].transfers:
										destroy_and_repair_steps[i].transfers.append(transfer)
									# aggiornare con true la lista dei task spacchettati
									for t in destroy_and_repair_steps[j].transfers:
										for k in AppData.transfers:
											if t.id_p == k.id_p and t.id_d == k.id_d:
												k.delivered = True
												k.q = t.q
									not_delivered = 0
							else:  # se sono in overload (non rispetto il vincolo della capacità)
								# controllo se lo step ha come nodo quello eliminato
								# i task del nodo eliminato li dobbiamo mettere nel nodo corrente
								if destroy_and_repair_steps[i].current_node.id == destroy_and_repair_steps[j].current_node.id:
									for transfer in destroy_and_repair_steps[j].transfers:
										destroy_and_repair_steps[i].transfers.append(transfer)
									# aggiornare con true la lista dei task spachettati
									for t in destroy_and_repair_steps[j].transfers:
										for k in AppData.transfers:
											if t.id_p == k.id_p and t.id_d == k.id_d:
												k.delivered = True
												k.q = t.q
									not_delivered = 0
								else:
									# calcolo costo overload
									overload = destroy_and_repair_steps[i].load / AppData.capacity  # restiruisce un 1,x dove x è la % di sforamento
									# calcolo costo viaggi con overload
									# n_over += 1
									if n_over == 0:
										destroy_and_repair_steps[i].overload = overload
									elif n_over == 1:
										destroy_and_repair_steps[i].overload = overload * 1.05
									elif n_over >= 3:
										destroy_and_repair_steps[i].overload = overload * 1.20
									elif n_over >= 5:
										destroy_and_repair_steps[i].overload = overload * 1.50
									n_over += 1

						if utils.controllo_consegne():
							# forse list out of rqnge quindi if AppData.set_solution != 0
							tot_l = AppData.len_set_solution[x]  # AppData.len_set_solution[len(AppData.len_set_solution) - 1]
							tot_l -= (utils.lenght(destroy_and_repair_steps[j].node_previous, destroy_and_repair_steps[j].current_node) + (utils.lenght(destroy_and_repair_steps[j].current_node, destroy_and_repair_steps[j].node_next)))
							if n_over > 0:
								tot_l += destroy_and_repair_steps[j].overload * (utils.lenght(destroy_and_repair_steps[j].node_previous, destroy_and_repair_steps[j].node_next))
								for step in range(j+1, i):
									tot_l -= utils.lenght(destroy_and_repair_steps[step].current_node, destroy_and_repair_steps[step].node_next)
									tot_l += destroy_and_repair_steps[step].overload * (utils.lenght(destroy_and_repair_steps[step].current_node, destroy_and_repair_steps[step].node_next))
							else:
								tot_l += (utils.lenght(destroy_and_repair_steps[j].node_previous, destroy_and_repair_steps[j].node_next))
							if tot_l > AppData.len_set_solution[x]:
								print('la soluzione è stata peggiorata = ' + str(tot_l))
								fail += 1  # se arrivo a 3 allora ho un ottimo locale
								del destroy_and_repair_steps[j]
								# aggiustamento della soluzione
								for h in range(j, len(destroy_and_repair_steps)):
									destroy_and_repair_steps[h].id -= 1
								destroy_and_repair_steps[j - 1].node_next = destroy_and_repair_steps[j].current_node
								destroy_and_repair_steps[j].node_previous = destroy_and_repair_steps[j-1].current_node
								# print new solution
								for step in destroy_and_repair_steps:
									print(step.current_node)
								print(destroy_and_repair_steps[0].current_node)
								AppData.set_solution.append(destroy_and_repair_steps)
								AppData.len_set_solution.append(tot_l)
								# vado a mettere True stop perchè ho aggiornato set_solution e aumento di 1 il numero di aggiornamenti
								x += 1
								stop = True
							else:
								print('la soluzione è stata migliorata = ' + str(tot_l))
								fail = 0  # resetto i fail per verificare se questa nuova soluzione è ottimo locale
								del destroy_and_repair_steps[j]
								# aggiustamento della soluzione
								for h in range(j, len(destroy_and_repair_steps)):
									destroy_and_repair_steps[h].id -= 1
								destroy_and_repair_steps[j - 1].node_next = destroy_and_repair_steps[j].current_node
								destroy_and_repair_steps[j].node_previous = destroy_and_repair_steps[j - 1].current_node
								# Aggiungo la nuova lista i step a set_solution e relativa total_lenght
								AppData.set_solution.append(destroy_and_repair_steps)
								AppData.len_set_solution.append(tot_l)
								# print new solution
								for step in destroy_and_repair_steps:
									print(step.current_node)
								print(destroy_and_repair_steps[0].current_node)
								x += 1
								stop = True
						else:
							print('Errore nelle consegne: tasks non ripartizionabili!')

					else:
						print('Non è possibile effettuare miglioramenti a partire dalla soluzione eliminando lo step: ' + str(destroy_and_repair_steps[j].id))

			# caso di ottimo locale
			if fail == 3:
				print('Questo test di destroy_and_repair porta ad un ottimo locale, perchè ho ottenuto ' + str(fail) + ' soluzioni peggiorate consecutive!')

			if utils.get_best_solution(AppData.set_solution, AppData.len_set_solution)[1] < AppData.len_set_solution[0]:
				# soluzione ottimizzata
				print('La soluzione ottimizzata dalla destroy & repair è: ' + str(utils.get_best_solution(AppData.set_solution, AppData.len_set_solution)[1]))
			else:
				print('La destroy & repair non è stata in grado di miglioare la soluzione della greedy!')
			print('Solution:')
			for count, step in enumerate(utils.get_best_solution(AppData.set_solution, AppData.len_set_solution)[0], 0):
				print(f'{count} --> ' + str(step.current_node.id))
			print(f'{count+1} --> 0 ')

			# incremento di 1 il numero di Destroy and Repair eseguite
			AppData.DR_counter += 1

		if choice == "GRASP":
			grasp_set_solition = []
			grasp_len_set_solution = []
			N: int = 0
			# repet for N times:
			while N < 100:
				print("Ripetizione Grasp numero: " + str(N))
				# rum greedy_random 1 volta:
				MenuHandler.serve(self, 'GREEDY_RANDOM')
				# run destroy_and_repair 1 volta:
				MenuHandler.serve(self, 'DESTROY_AND_REPAIR')
				# insert result in 2 apposite list:
				for solution in AppData.set_solution:
					grasp_set_solition.append(copy.deepcopy(solution))
				for len_solution in AppData.len_set_solution:
					grasp_len_set_solution.append(len_solution)
				# vari clear e reset per far ripartire in modo corretto la greedy-random, quindi la grasp
				AppData.steps.clear()
				AppData.nodes_in_solution.clear()
				AppData.q_d_n = 0
				# AppData.current_node = None
				AppData.set_solution.clear()
				AppData.len_set_solution.clear()
				# AppData.initial_nodes.clear()
				AppData.nodes.clear()
				utils.read_nodes_file()
				AppData.transfers.clear()
				utils.read_transfers_file()
				utils.upgrade_nodes_list()
				N += 1

			# avviare una funzione che controllo il risultato migliore e lo faccia vedere a video
			print("\nEnd Of Grasp:\n")
			print('Best solution:')
			# first version of print:
			# for count, step in enumerate(utils.get_best_solution(grasp_set_solition, grasp_len_set_solution)[0], 0):
			#	print(f'{count} --> ' + str(step.current_node.id))
			# print(f'{count+1} --> 0 ')
			# second version of print: (sistemare il for)
			for step in utils.get_best_solution(grasp_set_solition, grasp_len_set_solution)[0]:
				print(str(step.current_node.id), end=' -> ')
			print('0 ')
			print('Length = ', round(utils.get_best_solution(grasp_set_solition, grasp_len_set_solution)[1], 3))





