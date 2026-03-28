from pos.cli.current_sale_menu_cli import CurrentSaleMenuCLI
from pos.controller import Controller
from pos.exception.illegal_access_exception import IllegalAccessException
from pos.exception.illegal_operation_exception import IllegalOperationException

class SaleMenuCLI():

    def __init__(self, controller):
        self.controller = controller
        self.current_sale_menu_cli = CurrentSaleMenuCLI(self.controller)

    def sale_menu(self):
        while True:
            self.print_sale_menu()
            try:
                response = int(input('\nChoose your option: '))
            except ValueError:
                print('Please enter an integer number.')
                input('Type ENTER to continue.')
                continue
            if response == 1:
                self.initiate_sale()
                self.current_sale_menu_cli.current_sale_menu()
                input('Type ENTER to continue.')
            elif response == 2:
                self.search_sale()
                input('Type ENTER to continue.')
            elif response == 3:
                self.list_all_sales()
                input('Type ENTER to continue.')
            elif response == 4:
                self.print_existing_sale_receipt()
                input('Type ENTER to continue.')
            elif response == 5:
                print('\nRETURNING TO THE MAIN MENU.')
                break
            else:
                print('\nWRONG CHOICE. Please pick a choice between 1 and 5.')
                input('Type ENTER to continue.')
        return

    def print_sale_menu(self):
        print('\n\POINT OF SALES SYSTEM - SALE MENU\n\n')
        print('1 - Initiate sale')
        print('2 - Search sale by ID')
        print('3 - List all sales')
        print('4 - Print sale receipt of a previous sale')
        print('5 - Return to the main menu')

    def initiate_sale(self):
        print('INITIATE NEW SALE:\n')
        try:
            self.controller.initiate_sale()
            print('SALE INITIATED.\n')
        except IllegalAccessException:
            print('\nMUST LOGIN FIRST.')
        except IllegalOperationException:
            print('\nERROR INITIATING SALE.') 
            print('Cannot initiate sale with a sale in progress.')

    def search_sale(self):
        print('SEARCH SALE:\n')
        try:
            id = int(input('Enter the Sale ID: '))
            sale = self.controller.search_sale(id)
            if sale:
                self.print_sale_data(sale)
            else:
                print('\nThere is no sale registered with this ID.')
        except IllegalAccessException:
            print('\nMUST LOGIN FIRST.')

    def list_all_sales(self):
        print('LIST ALL SALES:\n')
        try:
            sales = self.controller.list_sales()
            if sales:
                for sale in sales:
                    print(sale)
            else:
                print('\nNo sales registered in the system.\n')
        except IllegalAccessException:
            print('\nMUST LOGIN FIRST.')

    # helper method to print sale data
    def print_sale_data(self, sale):
        print('\nSALE:')
        print(f'ID: {sale.id}')
        print(f'Date: {sale.date}')
        print(f'Net Sale: {sale.total:6.2f}')
        print(f'GST (5%): {sale.gst:6.2f}')
        print(f'PST (7%): {sale.pst:6.2f}')
        print(f'Total Sale: {sale.customer_total:6.2f}')
        print()

    def print_existing_sale_receipt(self):
        print('PRINT EXISTING SALE RECEIPT:\n')
        try:
            id = int(input('Enter the Sale ID: '))
            sale = self.controller.search_sale(id)
            if sale:
                print()
                print(sale.get_sale_receipt())
                print()
            else:
                print('\nThere is no sale registered with this ID.')
        except IllegalAccessException:
            print('\nMUST LOGIN FIRST.')
