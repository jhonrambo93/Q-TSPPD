from service.AppData import AppData
from step.Step import Step
import random
import utils
import copy
import time


class MenuHandler:

	def serve(self, choice: str) -> None:

		if choice == "GREEDY":

			# init
			log_file = open('log_file.txt', 'w+')
			AppData.total_length = 0
			step = 0
			border = []  # possibili nodi raggiungibili
			solution = []  # elenco dei nodi che compongono la soluzione, cioè il viaggio del furgoncino
			AppData.total_deliveries = 0  # totale consegne portate a termine
			load = 0  # carico nel furgone
			minimum_length = None

			# Start Greedy
			print('\nComputing ' + choice + ' . . .')
			start_time = time.time()
			AppData.initial_nodes = copy.deepcopy(AppData.nodes)  # copio la lista nodes in initial_nodes
			# Step 0
			AppData.current_node = AppData.nodes[0]  # impongo che il nodo iniziale è il nodo 0
			solution.append(AppData.current_node)

			for node in AppData.nodes:
				if node.q_p != 0:
					border.append(node)

			# Step 1
			step += 1
			log_file.write('Step: ' + str(step) + '\n')

			log_file.write('Calcolo delle distanze rispetto i nodi del border ... \n')

			# trovo il nodo più vicino
			nearest_n = utils.get_nearest_node(border, minimum_length)
			solution.append(nearest_n)
			AppData.nodes_in_solution.append(nearest_n)
			# Generarione Immagine della soluzione parziale
			# utils.images_sol_generation(solution)

			# Salvo ciò che viene fatto allo step 0
			AppData.steps.append(Step(0, AppData.current_node, None, nearest_n, copy.deepcopy(border), list(), 0, 0, 1))

			# aggiorno il nodo corrente, corrispondente allo step 1
			AppData.current_node = nearest_n

			minimum_length = None
			# carico il furgone della quantità del nodo corrente, se possibile
			if (load + AppData.current_node.q_p) <= AppData.capacity:
				load += AppData.current_node.q_p
				AppData.nodes[AppData.current_node.id].q_p = 0
				AppData.nodes[AppData.current_node.id].furgone = load
			else:
				print('ERROR in transfers file, node ' + str(AppData.current_node.id) + ' have q_p > ', str(AppData.capacity))
				exit()

			log_file.write('Nodo corrente:' + str(AppData.current_node) + '\n')
			log_file.write('Quantità nel furgone: ' + str(load) + '\n')

			border.clear()

			# Salvo ciò che viene fatto allo step 1
			AppData.steps.append(Step(1, AppData.current_node, AppData.steps[0].current_node, None, list(), list(), load, load, 1))

			# Other steps
			while utils.complete_deliveries(AppData.total_deliveries):
				step += 1
				log_file.write('\nStep: ' + str(step) + '\n')

				# border nodes generation
				border = utils.border_generation(border)

				log_file.write('Nodi frontiera, con i vincoli imposti:\n')
				for node in border:
					log_file.write(str(node) + '\n')

				log_file.write('Calcolo delle distanze rispetto i nodi di border ...\n')
				# trovo il nodo più vicino
				nearest_n = utils.get_nearest_node(border, minimum_length)
				solution.append(nearest_n)
				if nearest_n not in AppData.nodes_in_solution:
					AppData.nodes_in_solution.append(nearest_n)
				# Generarione Immagine della soluzione parziale
				# utils.images_sol_generation(solution)

				# Aggiorno border e nearest node dello step 1 o step precedente ad attuale se nel while
				AppData.steps[step-1].border = copy.deepcopy(border)
				AppData.steps[step-1].node_next = nearest_n

				AppData.current_node = nearest_n

				# step attuale, del while, primo aggiornamento#
				AppData.steps.append(Step(step, AppData.current_node, AppData.steps[step-1].current_node, None, list(), list(), load, 0, 1))

				minimum_length = None
				log_file.write('Nodo scelto: ' + str(nearest_n) + '\n')

				# scarico il furgone della quantità del nodo corrente, se deve ricevere dal nodo corrente
				load = utils.scarico_node(step, load, log_file)

				# carico il furgone della quantità del nodo corrente, se possibile
				load = utils.carico_node(step, load, log_file)

				log_file.write('\nQuantità nel furgone:' + str(load) + '\n')

				AppData.steps[step].load = load  # Update load of step

				log_file.write('Stato consegne: \n')
				for t in AppData.transfers:
					log_file.write(str(t) + '\n')

				border.clear()

			# Return to the deposit
			solution.append(AppData.nodes[0])
			# Show the solution
			print('\nSOLUTION: ')
			print('Sequence of node in solution:')
			for node in solution:
				print(node)
			print('\nTotal distance = ' + str(AppData.total_length))

			# Aggiorno next node del penultimo step (prima del ritorno al deposito)
			AppData.steps[step].node_next = solution[0]

			# Inserisco gli step della soluzione della greedy come primo elemento nella set_solutione
			# e relativa lunghezza in len_set_solution
			AppData.set_solution.append(AppData.steps)
			AppData.len_set_solution.append(AppData.total_length)

			# Generarione Immagine della soluzione definitiva
			utils.images_sol_generation(solution)

			# Show execution time
			ex_time = time.time() - start_time
			print('\n' + str(choice) + ' Execution time = ' + str(ex_time) + 'seconds')
			log_file.close()

		# ############################################################################################################
		# ############################################################################################################
		# ############################################################################################################

		if choice == "GREEDY_RANDOM":

			# init
			log_file = open('log_file.txt', 'w+')
			AppData.total_length = 0
			step = 0
			border = []  # possibili nodi raggiungibili
			solution = []  # elenco dei nodi che compongono la soluzione, cioè il viaggio del furgoncino
			AppData.total_deliveries = 0  # totale consegne portate a termine
			load = 0
			minimum_length = None

			# Start Greedy
			print('\nComputing ' + choice + ' . . .')
			start_time = time.time()
			AppData.initial_nodes = copy.deepcopy(AppData.nodes)  # copio la lista nodes in initial_nodes
			# Step 0
			AppData.current_node = AppData.nodes[0]  # impongo che il nodo iniziale è il nodo 0
			solution.append(AppData.current_node)

			for node in AppData.nodes:
				if node.q_p != 0:
					border.append(node)

			# Step 1
			step += 1
			log_file.write('Step: ' + str(step) + '\n')

			log_file.write('Calcolo delle distanze rispetto i nodi del border ... \n')

			# scelta nodo random
			j = random.randint(0, (len(border) - 1))
			nearest_n = border[j]
			AppData.total_length += utils.lenght(AppData.current_node, border[j])
			solution.append(nearest_n)
			AppData.nodes_in_solution.append(nearest_n)

			# Salvo ciò che viene fatto allo step 0
			AppData.steps.append(Step(0, AppData.current_node, None, nearest_n, copy.deepcopy(border), list(), 0, 0, 1))

			# aggiono il nodo corrente, corrispondente allo step 1
			AppData.current_node = nearest_n

			minimum_length = None
			# carico il furgone della quantità del nodo corrente, se possibile
			if (load + AppData.current_node.q_p) <= AppData.capacity:
				load += AppData.current_node.q_p
				AppData.nodes[AppData.current_node.id].q_p = 0
				AppData.nodes[AppData.current_node.id].furgone = load
			else:
				print('\nERROR in transfers file, node' + str(AppData.current_node.id) + ' have q_p > ', str(AppData.capacity))
				exit()

			log_file.write('Nodo corrente:' + str(AppData.current_node) + '\n')
			log_file.write('Quantità nel furgone: ' + str(load) + '\n')

			border.clear()

			# Salvo ciò che viene fatto allo step 1
			AppData.steps.append(Step(1, AppData.current_node, AppData.steps[0].current_node, None, list(), list(), load, load, 1))

			# Other steps
			while utils.complete_deliveries(AppData.total_deliveries):
				step += 1
				log_file.write('\nStep: ' + str(step) + '\n')

				# border nodes generation
				border = utils.border_generation(border)

				log_file.write('Nodi frontiera, con i vincoli imposti:\n')
				for node in border:
					log_file.write(str(node) + '\n')

				log_file.write('Calcolo delle distanze rispetto i nodi di border ...\n')
				# random node
				j = random.randint(0, (len(border) - 1))
				nearest_n = border[j]
				AppData.total_length += utils.lenght(AppData.current_node, border[j])
				solution.append(nearest_n)
				if nearest_n not in AppData.nodes_in_solution:
					AppData.nodes_in_solution.append(nearest_n)

				# Aggiorno border e nearest node dello step 1 o step precedente ad attuale se nel while
				AppData.steps[step-1].border = copy.deepcopy(border)
				AppData.steps[step-1].node_next = nearest_n

				AppData.current_node = nearest_n

				# step attuale, del while, primo aggiornamento
				AppData.steps.append(Step(step, AppData.current_node, AppData.steps[step-1].current_node, None, list(), list(), load, 0, 1))
				log_file.write('Nodo scelto: ' + str(nearest_n) + '\n')

				# scarico il furgone della quantità del nodo corrente, se deve ricevere dal nodo corrente
				load = utils.scarico_node(step, load, log_file)

				# carico il furgone della quantità del nodo corrente, se possibile
				load = utils.carico_node(step, load, log_file)

				log_file.write('\nQuantità nel furgone:' + str(load) + '\n')

				AppData.steps[step].load = load  # Update load of step

				log_file.write('Stato consegne: \n')
				for t in AppData.transfers:
					log_file.write(str(t) + '\n')

				border.clear()

			# Return to the deposit
			solution.append(AppData.nodes[0])
			# Show the solution
			# print('\nSOLUTION: ')
			# print('Sequence of node in solution:')
			# for node in solution:
			# print(node)
			# print('\nTotal distance = ' + str(AppData.total_length))

			# Aggiorno next node del penultimo step (prima del ritorno al deposito)
			AppData.steps[step].node_next = solution[0]

			# Inserisco gli step della soluzione della greedy come primo elemento nella set_solutione
			# e relativa lunghezza in len_set_solution
			AppData.set_solution.append(AppData.steps)
			AppData.len_set_solution.append(AppData.total_length)

			# Generarione Immagine della soluzione definitiva
			utils.images_sol_generation(solution)

			# Show execution time
			ex_time = time.time() - start_time
			print('\n' + str(choice) + ' Execution time = ' + str(ex_time) + 'seconds')
			log_file.close()

		# ############################################################################################################
		# ############################################################################################################
		# ############################################################################################################

		if choice == "GREEDY_BY_VALUE":

			# init
			log_file = open('log_file.txt', 'w+')
			AppData.total_length = 0
			step = 0
			border = []  # possibili nodi raggiungibili
			solution = []  # elenco dei nodi che compongono la soluzione, cioè il viaggio del furgoncino
			AppData.total_deliveries = 0  # totale consegne portate a termine
			load = 0  # carico nel furgone
			max_value = None

			# Start Greedy
			print('\nComputing ' + choice + ' . . .')
			start_time = time.time()
			AppData.initial_nodes = copy.deepcopy(AppData.nodes)  # copio la lista nodes in initial_nodes
			# Step 0
			AppData.current_node = AppData.nodes[0]  # impongo che il nodo iniziale è il nodo 0
			solution.append(AppData.current_node)

			for node in AppData.nodes:
				if node.q_p != 0:
					border.append(node)

			# Step 1
			step += 1
			log_file.write('Step: ' + str(step) + '\n')

			log_file.write('Calcolo delle distanze rispetto i nodi del border ... \n')

			if AppData.f_1:
				# trovo il nodo migliore con funzione 1
				best_n = utils.get_best_node(border, max_value, load)
			else:
				# trovo il nodo migliore con la funzione 2
				best_n = utils.get_best_node_2(border, max_value, load)

			solution.append(best_n)
			AppData.nodes_in_solution.append(best_n)

			# Salvo ciò che viene fatto allo step 0
			AppData.steps.append(Step(0, AppData.current_node, None, best_n, copy.deepcopy(border), list(), 0, 0, 1))

			# aggiono il nodo corrente, corrispondente allo step 1
			AppData.current_node = best_n

			max_value = None

			# carico il furgone della quantità del nodo corrente, se possibile
			if (load + AppData.current_node.q_p) <= AppData.capacity:
				load += AppData.current_node.q_p
				AppData.nodes[AppData.current_node.id].q_p = 0
				AppData.nodes[AppData.current_node.id].furgone = load
			else:
				print('ERROR in transfers file, node' + str(AppData.current_node.id) + ' have q_p > ', str(AppData.capacity))
				exit()

			log_file.write('Nodo corrente:' + str(AppData.current_node) + '\n')
			log_file.write('Quantità nel furgone: ' + str(load) + '\n')

			border.clear()

			# Salvo ciò che viene fatto allo step 1
			AppData.steps.append(Step(1, AppData.current_node, AppData.steps[0].current_node, None, list(), list(), load, load, 1))

			# Other steps
			while utils.complete_deliveries(AppData.total_deliveries):
				step += 1
				log_file.write('\nStep: ' + str(step) + '\n')

				# border nodes generation
				border = utils.border_generation(border)

				log_file.write('Nodi frontiera, con i vincoli imposti:\n')
				for node in border:
					log_file.write(str(node) + '\n')

					log_file.write('Calcolo valori funzione rispetto i nodi di border ...\n')
				# trovo il nodo migliore con la funzione 1
				# best_n = utils.get_best_node(border, max_value, load)

				# trovo il nodo migliore con la funzione 2
				best_n = utils.get_best_node_2(border, max_value, load)

				solution.append(best_n)
				AppData.nodes_in_solution.append(best_n)
				if best_n not in AppData.nodes_in_solution:
					AppData.nodes_in_solution.append(best_n)

				# Aggiorno border e nearest node dello step 1 o step precedente ad attuale se nel while
				AppData.steps[step - 1].border = copy.deepcopy(border)
				AppData.steps[step - 1].node_next = best_n

				AppData.current_node = best_n

				# step attuale, del while, primo aggiornamento
				AppData.steps.append(Step(step, AppData.current_node, AppData.steps[step - 1].current_node, None, list(), list(), load, 0, 1))

				max_value = None
				log_file.write('Nodo scelto: ' + str(best_n) + '\n')

				# scarico il furgone della quantità del nodo corrente, se deve ricevere dal nodo corrente
				load = utils.scarico_node(step, load, log_file)

				# carico il furgone della quantità del nodo corrente, se possibile
				load = utils.carico_node(step, load, log_file)

				log_file.write('\nQuantità nel furgone:' + str(load) + '\n')

				AppData.steps[step].load = load  # Update load of step

				log_file.write('Stato consegne: \n')
				for t in AppData.transfers:
					log_file.write(str(t) + '\n')

				border.clear()

			# Return to the deposit
			solution.append(AppData.nodes[0])
			# Show the solution
			print('\nSOLUTION: ')
			print('Sequence of node in solution:')
			for node in solution:
				print(node)
			print('\nTotal distance = ' + str(AppData.total_length))

			# Aggiorno next node del penultimo step (prima del ritorno al deposito)
			AppData.steps[step].node_next = solution[0]

			# Inserisco gli step della soluzione della greedy come primo elemento nella set_solutione
			# e relativa lunghezza in len_set_solution
			AppData.set_solution.append(AppData.steps)
			AppData.len_set_solution.append(AppData.total_length)

			# Generarione Immagine della soluzione definitiva
			utils.images_sol_generation(solution)

			# Show execution time
			ex_time = time.time() - start_time
			print('\n' + str(choice) + ' Execution time = ' + str(ex_time) + 'seconds')
			log_file.close()

		# ############################################################################################################
		# ############################################################################################################
		# ############################################################################################################

		if choice == "DESTROY_AND_REPAIR":

			# init
			DR_log_file = open('DR_log_file.txt', 'w+')
			x = 0
			not_delivered = 0
			fail = 0  # fail solution counter
			stop = False  # serve dopo aver trovato una nuova soluzione

			# Start Destroy and Repair
			print('\nComputing ' + choice + ' . . .')
			DR_start_time = time.time()
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
						DR_log_file.write('Step selected: ' + str(j) + '\n')
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
								DR_log_file.write('la soluzione è stata peggiorata = ' + str(tot_l) + '\n')
								fail += 1  # se arrivo a 3 allora ho un ottimo locale
								del destroy_and_repair_steps[j]
								# aggiustamento della soluzione
								for h in range(j, len(destroy_and_repair_steps)):
									destroy_and_repair_steps[h].id -= 1
								destroy_and_repair_steps[j - 1].node_next = destroy_and_repair_steps[j].current_node
								destroy_and_repair_steps[j].node_previous = destroy_and_repair_steps[j-1].current_node
								# print new solution
								for step in destroy_and_repair_steps:
									DR_log_file.write(str(step.current_node) + '\n')
								DR_log_file.write(str(destroy_and_repair_steps[0].current_node) + '\n')
								AppData.set_solution.append(destroy_and_repair_steps)
								AppData.len_set_solution.append(tot_l)
								# vado a mettere True stop perchè ho aggiornato set_solution e aumento di 1 il numero di aggiornamenti
								x += 1
								stop = True
							else:
								DR_log_file.write('la soluzione è stata migliorata = ' + str(tot_l) + '\n')
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
									DR_log_file.write(str(step.current_node) + '\n')
								DR_log_file.write(str(destroy_and_repair_steps[0].current_node) + '\n')
								x += 1
								stop = True
						else:
							DR_log_file.write('Errore nelle consegne: tasks non ripartizionabili!\n')

					else:
						DR_log_file.write('Non è possibile effettuare miglioramenti a partire dalla soluzione eliminando lo step: ' + str(destroy_and_repair_steps[j].id) + '\n')

			# caso di ottimo locale
			if fail == 3:
				print('Questo test di destroy_and_repair porta ad un ottimo locale, perchè ho ottenuto ' + str(fail) + ' soluzioni peggiorate consecutive!\n')

			if utils.get_best_solution(AppData.set_solution, AppData.len_set_solution)[1] < AppData.len_set_solution[0]:
				# soluzione ottimizzata
				print('La soluzione ottimizzata dalla destroy & repair è: ' + str(utils.get_best_solution(AppData.set_solution, AppData.len_set_solution)[1]))
				print('Solution:')
				for count, step in enumerate(utils.get_best_solution(AppData.set_solution, AppData.len_set_solution)[0], 0):
					print(f'{count} --> ' + str(step.current_node.id))
				print(f'{count+1} --> 0 ')
			else:
				print('La destroy & repair non è stata in grado di miglioare la soluzione della greedy!')
			# show execution time
			DR_ex_time = time.time() - DR_start_time
			print('\n' + str(choice) + ' Execution time = ' + str(DR_ex_time) + 'seconds')
			DR_log_file.close()

		# ############################################################################################################
		# ############################################################################################################
		# ############################################################################################################

		if choice == "GRASP":

			# init
			grasp_set_solition = []
			grasp_len_set_solution = []
			N: int = 0

			# Start Grasp
			print('\nComputing ' + choice + ' . . .')
			GRASP_start_time = time.time()

			# repet for N times:
			while N < 10:
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

			# show execution time
			GRASP_ex_time = time.time() - GRASP_start_time
			print('\n' + str(choice) + ' Execution time = ' + str(GRASP_ex_time) + 'seconds')

		# ############################################################################################################
		# ############################################################################################################
		# ############################################################################################################

		if choice == "BEST_IMPROVEMENT_D_&_R":

			# init
			new_set_solution = []
			new_len_set_solution = []
			N: int = 0
			num: int =0

			print("Please, insert the greedy type number: ")
			print('| <1> GREEDY              |')
			print('| <2> GREEDY_BY_VALUE     |')
			num = input()
			if num == '1':
				greedy_choice = 'GREEDY'
			elif num == '2':
				greedy_choice = 'GREEDY_BY_VALUE'

			# Start BEST_IMPROVEMT_DESTROY_AND_REPAIR
			print('\nComputing ' + choice + ' . . .')
			start_time = time.time()

			# repet for N times:
			while N < 100:
				print("Ripetizione numero: " + str(N))
				# rum greedy_random 1 volta:
				if N == 0:
					MenuHandler.serve(self, greedy_choice)
				# run destroy_and_repair 1 volta:
				MenuHandler.serve(self, 'DESTROY_AND_REPAIR')
				# insert result in 2 apposite list:
				for solution in AppData.set_solution:
					new_set_solution.append(copy.deepcopy(solution))
				for len_solution in AppData.len_set_solution:
					new_len_set_solution.append(len_solution)
				# vari clear e reset per far ripartire in modo corretto
				# AppData.steps.clear()
				# AppData.nodes_in_solution.clear()
				# AppData.q_d_n = 0
				# AppData.current_node = None
				if len(AppData.set_solution) > 1:
					k = len(AppData.set_solution)
					for i in range(1, k-1):
						del AppData.set_solution[1]
						del AppData.len_set_solution[1]
					del AppData.set_solution[1]
					del AppData.len_set_solution[1]
				# AppData.initial_nodes.clear()
				# AppData.nodes.clear()
				# utils.read_nodes_file()
				# AppData.transfers.clear()
				# utils.read_transfers_file()
				# utils.upgrade_nodes_list()
				N += 1

			# avviare una funzione che controllo il risultato migliore e lo faccia vedere a video
			print("\nEnd Of B_I_D_&_R:\n")
			print('Best solution:')
			for step in utils.get_best_solution(new_set_solution, new_len_set_solution)[0]:
				print(str(step.current_node.id), end=' -> ')
			print('0 ')
			print('Length = ', round(utils.get_best_solution(new_set_solution, new_len_set_solution)[1], 3))

			# show execution time
			ex_time = time.time() - start_time
			print('\n' + str(choice) + ' Execution time = ' + str(ex_time) + 'seconds')



