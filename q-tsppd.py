from service.Menu import Menu
from handler.MenuHandler import MenuHandler
from database import database

if __name__ == '__main__':

	print('   *******          **********  ******** *******  *******  *******  ')
	print('  **/////**        /////**///  **////// /**////**/**////**/**////** ')
	print(' **     //**           /**    /**       /**   /**/**   /**/**    /**')
	print('/**      /**  *****    /**    /*********/******* /******* /**    /**')
	print('/**    **/** /////     /**    ////////**/**////  /**////  /**    /**')
	print('//**  // **            /**           /**/**      /**      /**    ** ')
	print(' //******* **          /**     ******** /**      /**      /*******  ')
	print('  /////// //           //     ////////  //       //       ///////   ')

	DB_FILE = 'tsp.db'

	if not database.exist(DB_FILE):
		database.create_database(DB_FILE)
	else:
		database.reset_database(DB_FILE)

	database.fill_seeds(DB_FILE)

	Menu(MenuHandler()).show()
