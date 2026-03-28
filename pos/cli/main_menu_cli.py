from pos.configuration import Configuration
from pos.controller import Controller
from pos.cli.product_menu_cli import ProductMenuCLI
from pos.cli.sale_menu_cli import SaleMenuCLI

class MainMenuCLI():

	def __init__(self, controller):
		self.controller = controller
		self.product_menu_cli = ProductMenuCLI(self.controller)
		self.sale_menu_cli = SaleMenuCLI(self.controller)

	def main_menu(self):
		while True:
			self.print_main_menu()
			try:
				response = int(input('\nChoose your option: '))
			except ValueError:
				print('Please enter an integer number.')
				input('Type ENTER to continue.')
				continue
			if response == 1:
				self.product_menu_cli.product_menu()
			if response == 2:
				self.sale_menu_cli.sale_menu()
			elif response == 3:
				confirm = input('Are you sure you want to log out (y/n)? ')
				if confirm.lower() == 'y':
					break
			else:
				print('\nWRONG CHOICE. Please pick a choice between 1 and 3.')
				input('Type ENTER to continue.')
		return

	def print_main_menu(self):
		print('\n\nPOINT OF SALES SYSTEM\n\n')
		print('1 - Product Menu')
		print('2 - Sale Menu')
		print('3 - Log out')
