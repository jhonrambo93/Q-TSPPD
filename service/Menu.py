from handler.MenuHandler import MenuHandler


class Menu:

	def __init__(self, handler: MenuHandler):
		self.handler = handler

	def show(self) -> None:
		""" Shows the menu that interacts with the user

		:return: None
		"""

		choice = ''
		while choice != 'q':
			print('\n- Main Menù -----------------------')
			print('| <1>    |')
			print('| <2>    |')
			print('| <3>    |')
			print('| <4>    |')
			print('-----------------------------------')
			choice = input('Select an option (q to logout): ')

			if choice in {'1', '2', '3', '4'}:
				if choice == '1':
					command = ''
				elif choice == '2':
					command = ''
				elif choice == '3':
					command = ''
				elif choice == '4':
					command = ''

				self.handler.serve(command)

			elif choice == 'q':
					break
			elif choice != 'q':
				print('Input code is wrong. Choose one action!\n')
