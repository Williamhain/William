import sys
from pos.configuration import Configuration
from PyQt6 import QtCore, QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QWidget, QStackedLayout, QVBoxLayout, QPlainTextEdit
from pos.controller import Controller
from pos.exception.invalid_logout_exception import InvalidLogoutException
from pos.exception.invalid_login_exception import InvalidLoginException
from pos.exception.illegal_operation_exception import IllegalOperationException
from pos.exception.illegal_access_exception import IllegalAccessException
from pos.exception.no_current_sale_exception import NoCurrentSaleException
from pos.exception.invalid_product_exception import InvalidProductException

# creates a table that stores and displays the product data
class ProductTable(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            return self._data[index.row()][index.column()]

    def rowCount(self, index):
        return len(self._data)
    def columnCount(self, index):
        if len(self._data) == 0:
            return 0
        return len(self._data[0])

    def headerData(self, section, orientation, role):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                headers = ["UPC", "Product Name", "Price"]
                return headers[section]

# creates a table that stores and displays the sale data
class SaleTable(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            return self._data[index.row()][index.column()]

    def rowCount(self, index):
        return len(self._data)
        
    def columnCount(self, index):
        if len(self._data) == 0:
            return 0
        return len(self._data[0])

    def headerData(self, section, orientation, role):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                headers = ["Sale ID", "Date", "Customer Total"]
                return headers[section]

class PosGUI(QMainWindow):

    def __init__(self):
        super().__init__()
        # set autosave to True to ensure persistence is working
        self.configuration = Configuration()
        self.configuration.__class__.autosave = True
        # Continue here with your code!

        self.controller = Controller()
        self.setMinimumWidth(300)
        self.setWindowTitle("POS System")
        self.stack_layout = QStackedLayout()
        self.setup_login_page()
        self.setup_main_page()
        self.setup_create_product_page()
        self.setup_list_products_page()
        self.setup_retrieve_products_page()
        self.setup_search_product_page()
        self.setup_update_product_page()
        self.setup_delete_product_page()
        self.setup_sale_menu_page()
        self.setup_list_sales_page()
        self.setup_search_sale_page()

        container = QWidget()
        container.setLayout(self.stack_layout)
        self.setCentralWidget(container)
        self.stack_layout.setCurrentIndex(0)

    # sets up the login page, adding all necessary labels, inputs, layout, and the functionality to log in using a button
    def setup_login_page(self):
        self.login_page = QWidget()

        self.login_message_label = QLabel("POS System\n\nPlease enter your log in details:")
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password) # EchoMode hides the password as its being typed

        self.login_button = QPushButton("Log in")
        self.login_button.clicked.connect(self.login)
        self.login_button.setDefault(True)
        self.login_button.setAutoDefault(True)

        layout = QVBoxLayout()
        layout.addWidget(self.login_message_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)

        self.login_page.setLayout(layout)
        self.stack_layout.addWidget(self.login_page)

    # sets up the main page after logging in and creates logout button
    def setup_main_page(self):
        self.main_page = QWidget()

        self.main_message_label = QLabel("Logged in")
        self.logout_button = QPushButton("Log out")
        self.logout_button.clicked.connect(self.logout)
        self.create_product_page_button = QPushButton("Create Product")
        self.create_product_page_button.clicked.connect(self.switch_to_create_product_page)
        self.list_products_page_button = QPushButton("List All Products")
        self.list_products_page_button.clicked.connect(self.switch_to_list_products_page)
        self.retrieve_products_page_button = QPushButton("Retrieve Products")
        self.retrieve_products_page_button.clicked.connect(self.switch_to_retrieve_products_page)
        self.search_product_page_button = QPushButton("Search Product by UPC")
        self.search_product_page_button.clicked.connect(self.switch_to_search_product_page)
        self.update_product_page_button = QPushButton("Update Product Information")
        self.update_product_page_button.clicked.connect(self.switch_to_update_product_page)
        self.delete_product_page_button = QPushButton("Delete Product")
        self.delete_product_page_button.clicked.connect(self.switch_to_delete_product_page)
        self.sale_menu_page_button = QPushButton("Manage Sales")
        self.sale_menu_page_button.clicked.connect(self.switch_to_sale_menu_page)
        self.list_sales_page_button = QPushButton("List All Sales")
        self.list_sales_page_button.clicked.connect(self.switch_to_list_sales_page)
        self.search_sale_page_button = QPushButton("Search Sale by ID")
        self.search_sale_page_button.clicked.connect(self.switch_to_search_sale_page)

        layout = QVBoxLayout()
        layout.addWidget(self.main_message_label)
        layout.addWidget(self.logout_button)
        layout.addWidget(self.create_product_page_button)
        layout.addWidget(self.list_products_page_button)
        layout.addWidget(self.retrieve_products_page_button)
        layout.addWidget(self.search_product_page_button)
        layout.addWidget(self.update_product_page_button)
        layout.addWidget(self.delete_product_page_button)
        layout.addWidget(self.sale_menu_page_button)
        layout.addWidget(self.list_sales_page_button)
        layout.addWidget(self.search_sale_page_button)

        self.main_page.setLayout(layout)
        self.stack_layout.addWidget(self.main_page)

    # Handles the users login attempts and displays appropriate messages if log in is successful or not
    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        try:
            self.controller.login(username, password)
            self.login_message_label.setText("Login Successful!")
            self.username_input.clear()
            self.password_input.clear()
            self.stack_layout.setCurrentIndex(1)

        except InvalidLoginException:
            self.login_message_label.setText("Login incorrect")

    # Logs the user out, re prompts the log in message, then returns to the login page
    def logout(self):
     
        self.controller.logout()
        self.login_message_label.setText("POS System\n\nPlease enter your log in details")
        self.stack_layout.setCurrentIndex(0)

    # sets up the product page, adding all necessary labels, inputs, layout, and the functionality to create a new product and add
    # its description, price and UPC code. 
    def setup_create_product_page(self):
        self.create_product_page = QWidget()

        self.create_product_details_label = QLabel("Please enter new product details")

        self.upc_input = QLineEdit()
        self.upc_input.setPlaceholderText("UPC")
        self.description_input = QLineEdit()
        self.description_input.setPlaceholderText("Product Name")
        self.price_input = QLineEdit()
        self.price_input.setPlaceholderText("Price")

        self.create_product_button = QPushButton("Create Product")
        self.create_product_button.clicked.connect(self.create_product)
        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(self.switch_to_main_page)

        layout = QVBoxLayout()
        layout.addWidget(self.create_product_details_label)
        layout.addWidget(self.upc_input)
        layout.addWidget(self.description_input)
        layout.addWidget(self.price_input)
        layout.addWidget(self.create_product_button)
        layout.addWidget(self.back_button)

        self.create_product_page.setLayout(layout)
        self.stack_layout.addWidget(self.create_product_page)

    # sets up the product listing page adding all necessary labels, inputs, layout, and the functionality to list all products
    # and be able to return to the previous page. 
    def setup_list_products_page(self):
        self.list_products_page = QWidget()

        self.list_products_label = QLabel("All Products")
        self.product_table = QtWidgets.QTableView()
        self.back_button_list_products = QPushButton("Back")
        self.back_button_list_products.clicked.connect(self.switch_to_main_page)

        layout = QVBoxLayout()
        layout.addWidget(self.list_products_label)
        layout.addWidget(self.product_table)
        layout.addWidget(self.back_button_list_products)

        self.list_products_page.setLayout(layout)
        self.stack_layout.addWidget(self.list_products_page)

    # sets up the sales listing page adding all necessary labels, layout, and table
    def setup_list_sales_page(self):
        self.list_sales_page = QWidget()

        self.list_sales_label = QLabel("All Sales")
        self.sale_table = QtWidgets.QTableView()
        
        self.back_button_list_sales = QPushButton("Back")
        self.back_button_list_sales.clicked.connect(self.switch_to_main_page)

        layout = QVBoxLayout()
        layout.addWidget(self.list_sales_label)
        layout.addWidget(self.sale_table)
        layout.addWidget(self.back_button_list_sales)

        self.list_sales_page.setLayout(layout)
        self.stack_layout.addWidget(self.list_sales_page)

    # sets up the search sale page, adding labels, inputs, layout, and functionality to search for a sale by ID
    def setup_search_sale_page(self):
        self.search_sale_page = QWidget()

        self.search_sale_description = QLabel("Please enter a Sale ID to search for a specific transaction")
        
        self.search_sale_input = QLineEdit()
        self.search_sale_input.setPlaceholderText("Sale ID")
        
        self.search_sale_button = QPushButton("Search for Sale")
        self.search_sale_button.clicked.connect(self.search_sale)

        self.search_sale_table = QtWidgets.QTableView()

        self.back_button_search_sale = QPushButton("Back")
        self.back_button_search_sale.clicked.connect(self.switch_to_main_page)

        layout = QVBoxLayout()
        layout.addWidget(self.search_sale_description)
        layout.addWidget(self.search_sale_input)
        layout.addWidget(self.search_sale_button)
        layout.addWidget(self.search_sale_table)
        layout.addWidget(self.back_button_search_sale)

        self.search_sale_page.setLayout(layout)
        self.stack_layout.addWidget(self.search_sale_page)

    # switches to the main page
    def switch_to_main_page(self):
        self.stack_layout.setCurrentIndex(1)

    # switches to the create a product page
    def switch_to_create_product_page(self):
        self.create_product_details_label.setText("Please enter new product details")
        self.stack_layout.setCurrentIndex(2)

    # switches to the product listing page
    def switch_to_list_products_page(self):
        try:
            products = self.controller.list_products()

            list_data = []
            for product in products:
                list_data.append([product.upc, product.description, product.price])

            self.product_model = ProductTable(list_data)
            self.product_table.setModel(self.product_model)
            self.stack_layout.setCurrentIndex(3)
        except IllegalAccessException:
            self.main_message_label.setText("You must be logged in to view products.")

    # switches to the retrieve products page
    def switch_to_retrieve_products_page(self):
        self.retrieve_products_input.clear()
        self.retrieve_product_description.setText("Please enter a product name to search for a specific product")
        self.stack_layout.setCurrentIndex(4)

    # switches to the search product page
    def switch_to_search_product_page(self):
        self.search_product_input.clear()
        self.search_product_description.setText("Please enter a UPC code to search for a specific product")
        self.stack_layout.setCurrentIndex(5)

    # switches to the update product page
    def switch_to_update_product_page(self):
        self.original_upc_input.clear()
        self.updated_upc_input.clear()
        self.updated_description_input.clear()
        self.updated_price_input.clear()
        self.update_product_description.setText("Please enter the original UPC code of the product to be updated and enter the desired changes")
        self.stack_layout.setCurrentIndex(6)

    # switches to the delete product page
    def switch_to_delete_product_page(self):
        self.delete_product_input.clear()
        self.delete_product_description.setText("Please enter the UPC code of the product you wish to remove")
        self.stack_layout.setCurrentIndex(7)
    
    # swtiches to the sale menu page
    def switch_to_sale_menu_page(self):
        self.sale_status_label.setText("No active sale.")
        self.initiate_sale_button.setEnabled(True)
        self.stack_layout.setCurrentWidget(self.sale_menu_page)

    # switches to the sales listing page and retrieves data from the controller
    def switch_to_list_sales_page(self):
        try:
            sales = self.controller.list_sales()

            list_data = []
            for sale in sales:
                # If your Sale class uses different variable names, update them here!
                # You could also add more fields like the total price if you want.
                list_data.append([sale.id, sale.date, sale.customer_total])

            self.sale_model = SaleTable(list_data)
            self.sale_table.setModel(self.sale_model)
            
            # Use setCurrentWidget instead of index to avoid stacking order issues
            self.stack_layout.setCurrentWidget(self.list_sales_page) 
            
        except IllegalAccessException:
            self.main_message_label.setText("You must be logged in to view sales.")

    # switches to the search sale page and clears previous inputs
    def switch_to_search_sale_page(self):
        self.search_sale_input.clear()
        self.search_sale_description.setText("Please enter a Sale ID to search for a specific transaction")
        
        # Clear the table so old searches don't linger
        empty_model = SaleTable([])
        self.search_sale_table.setModel(empty_model)
        
        self.stack_layout.setCurrentWidget(self.search_sale_page)

    # creates a product using its UPC, description and price. If the price is not a number, throw an exception.
    def create_product(self):
        upc = self.upc_input.text()
        description = self.description_input.text()

        try:
            price = float(self.price_input.text())
        except ValueError:
            self.create_product_details_label.setText("Please input a number for the price")
            return
        
        try:
            self.controller.create_product(upc, description, price)
            self.create_product_details_label.setText("Product successfully created")
            self.upc_input.clear()
            self.description_input.clear()
            self.price_input.clear()

        except IllegalAccessException:
            self.create_product_details_label.setText("You must be logged in to create products")

    # sets up the retrieve products page, adding all necessary labels, inputs, layout, and the functionality to search for a specific product and press a button to
    # retrieve all matching products as well as go back to the main page
    def setup_retrieve_products_page(self):
        self.retrieve_products_page = QWidget()

        self.retrieve_product_description = QLabel("Please enter a product name to search for a specific product")
        self.retrieve_products_input = QLineEdit()
        self.retrieve_products_input.setPlaceholderText("Product Name")
        self.retrieve_products_button = QPushButton("Retrieve all products")
        self.retrieve_products_button.clicked.connect(self.retrieve_products)
        self.retrieve_products_table = QtWidgets.QTableView()
        self.back_button_retrieve_products = QPushButton("Back")
        self.back_button_retrieve_products.clicked.connect(self.switch_to_main_page)

        layout = QVBoxLayout()
        layout.addWidget(self.retrieve_product_description)
        layout.addWidget(self.retrieve_products_input)
        layout.addWidget(self.retrieve_products_button)
        layout.addWidget(self.retrieve_products_table)
        layout.addWidget(self.back_button_retrieve_products)

        self.retrieve_products_page.setLayout(layout)
        self.stack_layout.addWidget(self.retrieve_products_page)

    # searches for a specific product and if found appends it to the retrieve products list and then presents it as a table
    def retrieve_products(self):
        search = self.retrieve_products_input.text()
        try:
            products = self.controller.retrieve_products(search)
            retrieve_data = []
            for product in products:
                retrieve_data.append([product.upc, product.description, product.price])

            self.retrieve_product_model = ProductTable(retrieve_data)
            self.retrieve_products_table.setModel(self.retrieve_product_model)

        except IllegalAccessException:
            self.retrieve_product_description.setText("You must be logged in to retrieve products")

    # sets up the search product page, adding all necessary labels, inputs, layout, and the functionality to search for a product by its corresponding UPC code
    # and press a button to return to the main page
    def setup_search_product_page(self):
        self.search_product_page = QWidget()

        self.search_product_description = QLabel("Please enter a UPC code to search for a specific product")
        self.search_product_input = QLineEdit()
        self.search_product_input.setPlaceholderText("UPC")
        self.search_product_button = QPushButton("Search for Product")
        self.search_product_button.clicked.connect(self.search_product)

        self.search_product_table = QtWidgets.QTableView()

        self.back_button_search_product = QPushButton("Back")
        self.back_button_search_product.clicked.connect(self.switch_to_main_page)

        layout = QVBoxLayout()
        layout.addWidget(self.search_product_description)
        layout.addWidget(self.search_product_input)
        layout.addWidget(self.search_product_button)
        layout.addWidget(self.search_product_table)
        layout.addWidget(self.back_button_search_product)

        self.search_product_page.setLayout(layout)
        self.stack_layout.addWidget(self.search_product_page)

    # searches for a specific product via its UPC code and if found appends it to the search data list and then presents it as a table
    def search_product(self):
        upc = self.search_product_input.text()
        try:
            product = self.controller.search_product(upc)
            search_data = []
            if product is not None:
                search_data.append([product.upc, product.description, product.price])

            self.search_product_model = ProductTable(search_data)
            self.search_product_table.setModel(self.search_product_model)

        except IllegalAccessException:
            self.search_product_description.setText("You must be logged in to serach product")

    # sets up the update product page, adding all necessary labels, inputs, layout, and the functionality to update a product's name
    # price, and/or UPC code and a back button to be able to return to the main page
    def setup_update_product_page(self):
        self.update_product_page = QWidget()

        self.update_product_description = QLabel("Please enter the original UPC code of the product to be updated and enter the desired changes")
        self.original_upc_input = QLineEdit()
        self.original_upc_input.setPlaceholderText("Original UPC Code")
        self.updated_upc_input = QLineEdit()
        self.updated_upc_input.setPlaceholderText("New UPC Code")
        self.updated_description_input = QLineEdit()
        self.updated_description_input.setPlaceholderText("New Name")
        self.updated_price_input = QLineEdit()
        self.updated_price_input.setPlaceholderText("New Price")
        self.update_product_button = QPushButton("Update Product")
        self.update_product_button.clicked.connect(self.update_product)
        self.back_button_update_product = QPushButton("Back")
        self.back_button_update_product.clicked.connect(self.switch_to_main_page)

        layout = QVBoxLayout()
        layout.addWidget(self.update_product_description)
        layout.addWidget(self.original_upc_input)
        layout.addWidget(self.updated_upc_input)
        layout.addWidget(self.updated_description_input)
        layout.addWidget(self.updated_price_input)
        layout.addWidget(self.update_product_button)
        layout.addWidget(self.back_button_update_product)

        self.update_product_page.setLayout(layout)
        self.stack_layout.addWidget(self.update_product_page)

    # updates a product by allowing user to input the original UPC code of the product that they wish to update
    # and then modifying either the UPC code, price, or product name as desired. Does not allow negative numbers for prices
    # and only allows up to 2 decimal places. 
    def update_product(self):
        original_upc = self.original_upc_input.text()

        try:
            product = self.controller.search_product(original_upc)
        except IllegalOperationException:
            self.update_product_description.setText("Product does not exist")
            return
        except IllegalAccessException:
            self.update_product_description.setText("You must be logged in")
            return
        
        if product is None:
            self.update_product_description.setText("Product does not exist")
            return

        updated_upc = self.updated_upc_input.text()
        updated_description = self.updated_description_input.text()
        updated_price_text = self.updated_price_input.text()

        if updated_upc == "":
            updated_upc = product.upc

        if updated_description == "":
            updated_description = product.description

        if updated_price_text == "":
            updated_price = product.price
        else:
            try:
                updated_price = float(updated_price_text)

                if updated_price < 0:
                    self.update_product_description.setText("Price cannot be negative")
                    return

                if "." in updated_price_text:
                    decimal_part = updated_price_text.split(".")[1]
                    if len(decimal_part) > 2:
                        self.update_product_description.setText("Price can have at most 2 decimal places")
                        return

            except ValueError:
                self.update_product_description.setText("Please input a valid number for the price")
                return

        try:
            self.controller.update_product(original_upc, updated_upc, updated_description, updated_price)
            self.update_product_description.setText("Product successfully updated")
            self.original_upc_input.clear()
            self.updated_upc_input.clear()
            self.updated_description_input.clear()
            self.updated_price_input.clear()
        except IllegalOperationException:
            self.update_product_description.setText("This upc is already in use by product")
        except IllegalAccessException:
            self.update_product_description.setText("You must be logged in")

    # sets up the delete product page, adding all necessary labels, inputs, layout, and the functionality to delete a product via its UPC
    # code and a button to be able to return to the main page
    def setup_delete_product_page(self):
        self.delete_product_page = QWidget()

        self.delete_product_description = QLabel("Please enter the UPC code of the product you wish to remove")
        self.delete_product_input = QLineEdit()
        self.delete_product_input.setPlaceholderText("UPC")
        self.delete_product_button = QPushButton("Remove Product")
        self.delete_product_button.clicked.connect(self.delete_product)
        self.back_button_delete_product = QPushButton("Back")
        self.back_button_delete_product.clicked.connect(self.switch_to_main_page)

        layout = QVBoxLayout()
        layout.addWidget(self.delete_product_description)
        layout.addWidget(self.delete_product_input)
        layout.addWidget(self.delete_product_button)
        layout.addWidget(self.back_button_delete_product)

        self.delete_product_page.setLayout(layout)
        self.stack_layout.addWidget(self.delete_product_page)

    # sets up the sale menu page, including labels for sale status, 
    # buttons to initiate a new sale, and navigation to return to the main menu.
    def setup_sale_menu_page(self):
        self.sale_menu_page = QWidget()
        sale_layout = QVBoxLayout()
        
        self.sale_status_label = QLabel("No active sale.")

        self.initiate_sale_button = QPushButton("Initiate New Sale")
        self.initiate_sale_button.clicked.connect(self.initiate_sale)
        
        # button to cancel the current active sale
        self.cancel_sale_button = QPushButton("Cancel Current Sale")
        self.cancel_sale_button.clicked.connect(self.cancel_sale)

        # add item section
        self.add_item_label = QLabel("Add Item to Sale:")
        
        self.sale_upc_input = QLineEdit()
        self.sale_upc_input.setPlaceholderText("Enter Product UPC")
        
        self.sale_quantity_input = QLineEdit()
        self.sale_quantity_input.setPlaceholderText("Enter Quantity (e.g., 1 or 2.5)")
        
        self.add_item_button = QPushButton("Add Item")
        self.add_item_button.clicked.connect(self.add_item_to_sale)

        # Finish Sale Button
        self.finish_sale_button = QPushButton("Finish Current Sale")
        self.finish_sale_button.clicked.connect(self.finish_sale)

        # receipt display area
        self.receipt_display = QPlainTextEdit()
        self.receipt_display.setReadOnly(True) 
        self.receipt_display.setPlaceholderText("Items added to the current sale will appear here")

        # add a back button so you can return to the main menu
        self.back_button_sale_menu = QPushButton("Back")
        self.back_button_sale_menu.clicked.connect(self.switch_to_main_page)

        sale_layout.addWidget(self.sale_status_label)
        sale_layout.addWidget(self.initiate_sale_button)
        sale_layout.addWidget(self.cancel_sale_button)
        
        # add the new inputs to the layout
        sale_layout.addWidget(self.add_item_label)
        sale_layout.addWidget(self.sale_upc_input)
        sale_layout.addWidget(self.sale_quantity_input)
        sale_layout.addWidget(self.add_item_button)
        sale_layout.addWidget(self.finish_sale_button)
        sale_layout.addWidget(self.receipt_display)
        sale_layout.addWidget(self.back_button_sale_menu)

        self.sale_menu_page.setLayout(sale_layout)
        self.stack_layout.addWidget(self.sale_menu_page)

    # deletes a product via its UPC code and throw an exception if the product does not exist
    def delete_product(self):
        upc = self.delete_product_input.text()

        try:
            self.controller.delete_product(upc)
            self.delete_product_description.setText("Product removed successfully")
            self.delete_product_input.clear()

        except IllegalOperationException:
            self.delete_product_description.setText("Specified product does not exist")
        except IllegalAccessException:
            self.delete_product_description.setText("You must be logged in")

    # Initiates a new sale and handles exceptions
    def initiate_sale(self):
        try:
            self.controller.initiate_sale()
            self.sale_status_label.setText("New sale initiated in progress")
            self.initiate_sale_button.setEnabled(False) # Disable the button so they don't click it twice by accident
            self.receipt_display.clear() # Clear receipt for the new sale

        except IllegalAccessException:
            self.sale_status_label.setText("You must be logged in to initiate a sale.")
        except IllegalOperationException:
            self.sale_status_label.setText("A sale is already in progress. Please finish or cancel it first.")

    # cancels the active sale and resets the UI status
    def cancel_sale(self):
        try:
            self.controller.cancel_current_sale()
            self.sale_status_label.setText("No active sale.")       
            self.initiate_sale_button.setEnabled(True) # re-enable the initiate button so a new sale can be started
            self.receipt_display.clear() # Clear the cancelled items

        except IllegalAccessException:
            self.sale_status_label.setText("You must be logged in to cancel a sale.")
        except NoCurrentSaleException:
            self.sale_status_label.setText("There is no active sale to cancel.")

    # Adds a product to the active sale
    def add_item_to_sale(self):
        upc = self.sale_upc_input.text().strip()
        quantity_str = self.sale_quantity_input.text().strip()

        if not upc or not quantity_str:
            self.sale_status_label.setText("Please enter both a UPC and a Quantity.")
            return

        try:
            quantity = float(quantity_str)

            if quantity <= 0:
                raise ValueError()
            
            self.controller.add_new_sale_line_item(quantity, upc)
            
            # Fetch updated items and display them
            current_items = self.controller.print_sale_line_items()
            if current_items:
                self.receipt_display.setPlainText(current_items)

            self.sale_status_label.setText(f"Added item (UPC: {upc}) to the sale.") 

            # Clear inputs for the next item
            self.sale_upc_input.clear()
            self.sale_quantity_input.clear()
            
        except ValueError:
            self.sale_status_label.setText("Quantity must be a valid number.")
        except IllegalAccessException:
            self.sale_status_label.setText("You must be logged in to add items.")
        except NoCurrentSaleException:
            self.sale_status_label.setText("You must initiate a sale before adding items.")
        except InvalidProductException:
            self.sale_status_label.setText("Product not found. Please check the UPC.")     

    # Finishes the current sale and displays the final receipt
    def finish_sale(self):
        try:
            finished_sale = self.controller.finish_current_sale()
            
            # Display the final receipt
            self.receipt_display.setPlainText(finished_sale.get_sale_receipt())
            self.sale_status_label.setText("The sale has been concluded!")
            self.initiate_sale_button.setEnabled(True)
            
        except NoCurrentSaleException:
            self.sale_status_label.setText("There is no active sale to finish.")
        except IllegalOperationException:
            self.sale_status_label.setText("Cannot finish a sale with no items.")
        except IllegalAccessException:
            self.sale_status_label.setText("You must be logged in to finish a sale.")

    # searches for a specific sale via its ID and presents it in the table
    def search_sale(self):
        sale_id_str = self.search_sale_input.text().strip()
        
        if not sale_id_str:
            self.search_sale_description.setText("Please enter a Sale ID.")
            return

        try:
            # Depending on how the controller is written, ID might need to be an int
            try:
                sale_id = int(sale_id_str)
            except ValueError:
                sale_id = sale_id_str # Fallback to string if IDs are alphanumeric

            sale = self.controller.search_sale(sale_id)
            
            search_data = []
            if sale is not None:
                # Using the exact variables we verified: id, date, customer_total
                search_data.append([sale.id, sale.date, sale.customer_total])
                self.search_sale_description.setText(f"Found Sale ID {sale_id}")
            else:
                self.search_sale_description.setText(f"No sale found with ID {sale_id}")

            self.search_sale_model = SaleTable(search_data)
            self.search_sale_table.setModel(self.search_sale_model)
            
        except IllegalAccessException:
            self.search_sale_description.setText("You must be logged in to search sales.")
        except Exception as e:
            self.search_sale_description.setText(f"Error occurred during search: {e}")

def main():
    app = QApplication(sys.argv)
    window = PosGUI()
    window.show()
    app.exec()

if __name__ == '__main__':
    main()
