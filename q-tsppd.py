from service.AppData import AppData
from service.Menu import Menu
from handler.MenuHandler import MenuHandler
from node.Node import Node
from transfer.Transfer import Transfer


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
	f = open('nodes.txt', 'r')
	for line in f:
		parts = line.split()
		# print(parts)
		AppData.nodes.append(Node(int(parts[0]), float(parts[1]), float(parts[2])))
	# for node in AppData.nodes:
	# print(node)
	f.close()

	# read transfers file
	# f = open('transfers.txt', 'r')
	f = open('transfers2.txt', 'r')
	for line in f:
		parts = line.split()
		# print(parts)
		AppData.transfers.append(Transfer(int(parts[0]), int(parts[1]), int(parts[2]), False))
	# for node in nodes:
	# print(node)
	f.close()

	# upgrade nodes list
	for node in AppData.nodes:
		if node.id != 0:
			for transfer in AppData.transfers:
				if transfer.id_p == node.id:
					node.q_p = node.q_p + transfer.q
				elif transfer.id_d == node.id:
					node.q_d = node.q_d + transfer.q
	# for node in AppData.nodes:
	# print(node)

	Menu(MenuHandler()).show()
