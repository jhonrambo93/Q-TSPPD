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
	Menu(MenuHandler()).show()
