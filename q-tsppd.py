from service.AppData import AppData
from service.Menu import Menu
from handler.MenuHandler import MenuHandler
import utils
import matplotlib.pylab as plt
import numpy as np


if __name__ == '__main__':

	print('\n ')
	print('   *******          **********  ********  *******   *******   *******  ')
	print('  **/////**        /////**///  **//////  /**////** /**////** /**////** ')
	print(' **     //**           /**    /**        /**   /** /**   /** /**    /**')
	print('/**      /**  *****    /**    /********* /*******  /*******  /**    /**')
	print('/**    **/** /////     /**    ////////** /**////   /**////   /**    /**')
	print('//**  // **            /**           /** /**       /**       /**    ** ')
	print(' //******* **          /**     ********  /**       /**       /*******  ')
	print('  /////// //           //     ////////   //        //        ///////   ')

	if AppData.testing:
		# generazione random dei file
		utils.project_file_generation()
		# read nodes file
		AppData.file_nodes = 'node/n_file/nodesTest.txt'
		utils.read_nodes_file()
		# read transfers file
		AppData.file_transfers = 'transfer/t_file/transfersTest.txt'
		utils.read_transfers_file()
	else:
		# read nodes file
		AppData.file_nodes = 'node/n_file/nodes.txt'
		utils.read_nodes_file()
		# read transfers file
		AppData.file_transfers = 'transfer/t_file/transfers.txt'
		utils.read_transfers_file()

	# upgrade nodes list
	utils.upgrade_nodes_list()

	for node in AppData.nodes:
		AppData.total_trasfer += node.q_d
	print(str(AppData.total_trasfer))

	# graph generation
	all_nodes = AppData.nodes[:]
	d = all_nodes[0]
	x_max = 0
	y_max = 0
	# deposito
	deposito = [(d.x, d.y)]
	deposito = np.array(deposito)
	all_nodes.remove(all_nodes[0])
	# nodes
	nodo = [(n.x, n.y) for n in all_nodes]
	nodo = np.array(nodo)
	plt.plot(deposito[0, 0], deposito[0, 1], 'bD', nodo[:, 0], nodo[:, 1], 'ro')

	# graph configuration
	plt.xlabel('X')
	plt.ylabel('Y')
	# imposto le dimensioni del grafico
	for n in AppData.nodes:
		if n.x > x_max:
			x_max = n.x
		if n.y > y_max:
			y_max = n.y
	x_max = x_max*1.4
	y_max = y_max*1.4
	plt.axis([-5, x_max, -5, y_max])
	plt.axis('on')
	plt.grid()
	plt.title('Titolo Grafo')
	plt.savefig('images/Grafo.png')
	# plt.show()

	Menu(MenuHandler()).show()

