from pos.controller import Controller
from pos.exception.invalid_logout_exception import InvalidLogoutException
from pos.exception.illegal_access_exception import IllegalAccessException
from pos.exception.illegal_operation_exception import IllegalOperationException

class ProductMenuCLI():

    def __init__(self, controller):
        self.controller = controller


    def product_menu(self):
        while True:
            self.print_product_menu()
            try:
                response = int(input('\nChoose your option: '))
            except ValueError:
                print('Please enter an integer number.')
                input('Type ENTER to continue.')
                continue
            if response == 1:
                self.create_product()
                input('Type ENTER to continue.')
            elif response == 2:
                self.search_product()
                input('Type ENTER to continue.')
            elif response == 3:
                self.retrieve_products_by_description()
                input('Type ENTER to continue.')
            elif response == 4:
                self.update_product()
                input('Type ENTER to continue.')
            elif response == 5:
                self.delete_product()
                input('Type ENTER to continue.')
            elif response == 6:
                self.list_all_products()
                input('Type ENTER to continue.')
            elif response == 7:
                print('\nRETURNING TO THE MAIN MENU.')
                break
            else:
                print('\nWRONG CHOICE. Please pick a choice between 1 and 7.')
                input('Type ENTER to continue.')
        return

    def print_product_menu(self):
        print('\n\nPOINT OF SALES SYSTEM - PRODUCT MENU\n\n')
        print('1 - Add new product')
        print('2 - Search product by UPC')
        print('3 - Retrieve products by text')
        print('4 - Change product data')
        print('5 - Remove product')
        print('6 - List all products')
        print('7 - Return to the main menu')

    def create_product(self):
        print('ADD NEW PRODUCT:')
        try:
            upc = input('Enter the Product UPC: ')
            description = input('Product description: ')
            price = float(input('Product price: '))
            self.controller.create_product(upc, description, price)
            print('\nPRODUCT ADDED TO THE SYSTEM.')
        except IllegalAccessException:
            print('\nMUST LOGIN FIRST.')
        except IllegalOperationException:
            print('\nERROR ADDING NEW PRODUCT.') 
            print('There is a product already registered with UPC %s.' % upc)

    def search_product(self):
        print('SEARCH PRODUCT:')
        try:
            upc = input('Enter the Product UPC: ')
            product = self.controller.search_product(upc)
            if product:
                self.print_product_data(product)
            else:
                print('\nThere is no product registered with this UPC.')
        except IllegalAccessException:
            print('\nMUST LOGIN FIRST.')

    # helper method to print product data
    def print_product_data(self, product):
        print('\nPRODUCT:')
        print('UPC: %s' % product.upc)
        print('Description: %s' % product.description)
        print('Price: %.2f' % product.price)
        print()

    def retrieve_products_by_description(self):
        print('RETRIEVE PRODUCTS BY TEXT:')
        try:
            search_string = input('Search for: ')
            found_products = self.controller.retrieve_products(search_string)
            if found_products:
                print('\nProducts found with text %s:\n' % search_string)
                for product in found_products:
                    print(product)
            else:
                print('\nNo products found with text: %s\n' % search_string)
        except IllegalAccessException:
            print('\nMUST LOGIN FIRST.')


    def update_product(self):
        print('CHANGE PRODUCT DATA:')
        try:
            original_upc = input('Enter the Product UPC: ')
            product = self.controller.search_product(original_upc)
            if product:
                self.print_product_data(product)
                print('Type the new data value or enter for each field that should keep the old data: ')
                upc = input('Product UPC: ')
                description = input('Product description: ')
                price = input('Product price: ')

                # update only fields that were not empty
                upc = upc if upc !='' else product.upc
                description = description if description !='' else product.description
                price = float(price) if price !='' else product.price

                confirm = input('\nAre you sure you want to change product data %s (y/n)? ' % product.description)
                if confirm.lower() == 'y':
                    self.controller.update_product(original_upc, upc, description, price)
                    print('\nPRODUCT DATA CHANGED.')
            else:
                print('\nERROR CHANGING PRODUCT DATA.')
                print('There is no product registered with this UPC.')
        except IllegalAccessException:
            print('\nMUST LOGIN FIRST.')
        except IllegalOperationException:
            print('\nERROR CHANGING PRODUCT DATA.')
            print('Cannot change product data to a new UPC that is already registered in the system.')


    def delete_product(self):
        print('REMOVE PRODUCT:')
        try:
            upc = input('Enter the Product UPC: ')
            product = self.controller.search_product(upc)
            if product:
                self.print_product_data(product)
                confirm = input('\nAre you sure you want to remove product %s (y/n)? ' % product.description)
                if confirm.lower() == 'y':
                    self.controller.delete_product(upc)
                    print('\nPRODUCT REMOVED FROM THE SYSTEM.')
            else:
                print('\nERROR REMOVING PRODUCT.')
                print('There is no product registered with this UPC.')
        except IllegalAccessException:
            print('\nMUST LOGIN FIRST.')
        except IllegalOperationException:
            print('\nERROR REMOVING PRODUCT.')
            print('Cannot remove a product that is not registered in the system.')

    def list_all_products(self):
        print('LIST ALL PRODUCTS:\n')
        try:
            products = self.controller.list_products()
            if products:
                for product in products:
                    print(product)
            else:
                print('\nNo products registered in the system.\n')
        except IllegalAccessException:
            print('\nMUST LOGIN FIRST.')

