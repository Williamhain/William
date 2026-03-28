from pos.controller import Controller
from pos.exception.illegal_access_exception import IllegalAccessException
from pos.exception.illegal_operation_exception import IllegalOperationException
from pos.exception.invalid_product_exception import InvalidProductException
from pos.exception.no_current_sale_exception import NoCurrentSaleException

class CurrentSaleMenuCLI():

    def __init__(self, controller):
        self.controller = controller

    def current_sale_menu(self):
        while True:
            self.print_current_sale_menu()
            try:
                response = int(input('\nChoose your option: '))
            except ValueError:
                print('Please enter an integer number.')
                input('Type ENTER to continue.')
                continue
            if response == 1:
                self.add_new_sale_line_item()
                input('Type ENTER to continue.')
            elif response == 2:
                if self.finish_current_sale():
                    break
                else:
                    input('Type ENTER to continue.')
            elif response == 3:
                if self.cancel_current_sale():
                    break
                else:
                    input('Type ENTER to continue.')
            else:
                print('\nWRONG CHOICE. Please pick a choice between 1 and 4.')
                input('Type ENTER to continue.')
        return

    def print_current_sale_menu(self):
        print('\nPOINT OF SALES SYSTEM - CURRENT SALE MENU\n\n')
        print('1 - Add item to the current sale')
        print('2 - Finish current sale')
        print('3 - Cancel current sale')

    def add_new_sale_line_item(self):
        print('ADD ITEM TO THE CURRENT SALE:\n')
        try:
            quantity = float(input('Quantity: '))
            upc = input('Scan/Type the Product UPC: ')
            sale_line_item = self.controller.add_new_sale_line_item(quantity, upc)
            print('Registered:', end=' ')
            print(self.controller.print_sale_line_item(sale_line_item.code))
        except IllegalAccessException:
            print('\nMUST LOGIN FIRST.')
        except NoCurrentSaleException:
            print('\nERROR ADDING ITEM.')
            print('Cannot add item without a current sale in progress.')
        except InvalidProductException:
            print('\nERROR ADDING ITEM.')
            print('Invalid Product: Must be a valid UPC registered in the system.')

    def finish_current_sale(self):
        print('FINISH CURRENT SALE:\n')
        confirm = input('Are you sure you want to conclude the current sale (y/n)? ')
        if confirm.lower() == 'y':
            try:
                finished_sale = self.controller.finish_current_sale()
                print('\nCURRENT SALE CONCLUDED.')
                print('PRINTING RECEIPT...\n')
                print(finished_sale.get_sale_receipt())
                return True
            except IllegalAccessException:
                print('\nMUST LOGIN FIRST.')
            except NoCurrentSaleException:
                print('\nERROR FINISHING SALE.')
                print('Cannot finish a sale without a current sale in progress.')
            except IllegalOperationException:
                print('\nERROR FINISHING SALE.')
                print('Cannot finish a sale without adding at least one item.')
        return False

    def cancel_current_sale(self):
        print('CANCEL CURRENT SALE:\n')
        confirm = input('Are you sure you want to cancel the current sale (y/n)? ')
        if confirm.lower() == 'y':
            try:
                self.controller.cancel_current_sale()
                print('\nCURRENT SALE CANCELLED.')
                return True
            except IllegalAccessException:
                print('\nMUST LOGIN FIRST.')
            except NoCurrentSaleException:
                print('\nERROR CANCELLING SALE.')
                print('Cannot cancel a sale without a current sale in progress.')
        return False
