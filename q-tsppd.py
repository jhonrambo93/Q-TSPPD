from service.AppData import AppData
from service.Menu import Menu
from handler.MenuHandler import MenuHandler
import utils


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
	AppData.file_nodes = 'nodes.txt'
	utils.read_nodes_file()

	# read transfers file
	AppData.file_transfers = 'transfers0.txt'
	utils.read_transfers_file()

	# upgrade nodes list
	utils.upgrade_nodes_list()

	# for node in AppData.nodes:
	# print(node)

	Menu(MenuHandler()).show()
