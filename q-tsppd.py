from service.Menu import Menu
from handler.MenuHandler import MenuHandler
from node import Node

if __name__ == '__main__':

	print('   *******          **********  ******** *******  *******  *******  ')
	print('  **/////**        /////**///  **////// /**////**/**////**/**////** ')
	print(' **     //**           /**    /**       /**   /**/**   /**/**    /**')
	print('/**      /**  *****    /**    /*********/******* /******* /**    /**')
	print('/**    **/** /////     /**    ////////**/**////  /**////  /**    /**')
	print('//**  // **            /**           /**/**      /**      /**    ** ')
	print(' //******* **          /**     ******** /**      /**      /*******  ')
	print('  /////// //           //     ////////  //       //       ///////   ')

	# read nodes file
	nodes = []
	f = open('nodes.txt', 'r')
	for line in f:
		parts = line.split()
		# print(parts)
		nodes.append(Node.Node(int(parts[0]), float(parts[1]), float(parts[2])))
	# for node in nodes:
	# print(node)
	# print('ok lettura file nodi')
	f.close()

	# read transfers file
	transfers = []
	f = open('transfers.txt', 'r')
	for line in f:
		parts = line.split()
		# print(parts)
		transfers.append((int(parts[0]), int(parts[1]), int(parts[2])))
	# for node in nodes:
	# print(node)
	# print('ok lettura file nodi')
	f.close()

	# upgrade nodes list
	for node in nodes:
		if node.id != 0:
			for transfer in transfers:
				if transfer[0] == node.id:
					node.q_p = node.q_p + transfer[2]
				elif transfer[1] == node.id:
					node.q_d = node.q_d + transfer[2]
	# for node in nodes:
	# print(node)

	# greedy least distance


	Menu(MenuHandler()).show()
