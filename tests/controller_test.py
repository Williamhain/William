from unittest import TestCase
from unittest import main
from datetime import date, datetime
from pos.controller import Controller
from pos.product import Product
from pos.sale import Sale
from pos.sale_line_item import SaleLineItem
from pos.configuration import Configuration
from pos.exception.invalid_login_exception import InvalidLoginException
from pos.exception.duplicate_login_exception import DuplicateLoginException
from pos.exception.invalid_logout_exception import InvalidLogoutException
from pos.exception.illegal_access_exception import IllegalAccessException
from pos.exception.illegal_operation_exception import IllegalOperationException
from pos.exception.no_current_sale_exception import NoCurrentSaleException
from pos.exception.invalid_product_exception import InvalidProductException

class ControllerTest(TestCase):

	def setUp(self):
		# set autosave to False to ignore testing persistence
		self.configuration = Configuration()
		self.configuration.__class__.autosave = False
		self.controller = Controller()


	def test_login_logout(self):
		with self.assertRaises(InvalidLogoutException, msg="log out only after being logged in"):
			self.controller.logout()
		with self.assertRaises(InvalidLoginException, msg="login in with incorrect username"):
			self.controller.login("incorrectuser", "123456")
		with self.assertRaises(InvalidLoginException, msg="login in with incorrect password"):
			self.controller.login("user", "abadpassword")
		self.assertTrue(self.controller.login("user", "123456"), "login correctly")
		with self.assertRaises(DuplicateLoginException, msg="cannot login again while still logged in"):
			self.controller.login("user", "123456")
		self.assertTrue(self.controller.logout(), "log out correctly")
		self.assertTrue(self.controller.login("user", "123456"), "can login again")
		self.assertTrue(self.controller.logout(), "can log out again")
		self.assertTrue(self.controller.login("ali", "@G00dPassw0rd"), "another user logging in")
		self.assertTrue(self.controller.logout(), "can log out again")


	def test_create_search_product(self):
		# some products that will be created
		expected_product_1 = Product("037466022680", "Lindt Excellence Orange", 4.99)
		expected_product_2 = Product("629070500083", "Kicking Horse Coffee", 18.99)
		expected_product_3 = Product("000000003294", "BC Jazz Apple per kg", 5.93)

		# cannot do operation without logging in
		with self.assertRaises(IllegalAccessException, msg="cannot search product without logging in"):
			self.controller.search_product("037466022680")
		with self.assertRaises(IllegalAccessException, msg="cannot create product without logging in"):
			self.controller.create_product("037466022680", "Lindt Excellence Orange", 4.99)

		# add one product
		self.assertTrue(self.controller.login("user", "123456"), "login correctly")
		actual_product = self.controller.create_product("037466022680", "Lindt Excellence Orange", 4.99)
		self.assertIsNotNone(actual_product, "product created cannot be null")

		# implement __eq__(self, other) in Product to compare products based on its attributes
		self.assertEqual(expected_product_1, actual_product, "Lindt Excellence Orange product was created and their data are correct")

		# after creating the product, one should be able to search it
		actual_product = self.controller.search_product("037466022680")
		self.assertIsNotNone(actual_product, "product created and retrieved cannot be null")
		self.assertEqual(expected_product_1, actual_product, "Lindt Excellence Orange product was created, retrieved and its data are correct")

		# should not allow to create another product with same upc
		with self.assertRaises(IllegalOperationException, msg="cannot create product with same upc that is already registered"):
			self.controller.create_product("037466022680", "Kicking Horse Coffee", 18.99)

		# add a second product
		actual_product = self.controller.create_product("629070500083", "Kicking Horse Coffee", 18.99)
		self.assertIsNotNone(actual_product, "second product created cannot be null")
		self.assertEqual(expected_product_2, actual_product, "second product, Kicking Horse Coffee, was created and its data are correct")
		actual_product = self.controller.search_product("629070500083")
		self.assertIsNotNone(actual_product, "product created and retrieved cannot be null")
		self.assertEqual(expected_product_2, actual_product, "second product, Kicking Horse Coffee, was created, retrieved and its data are correct")

		# add a third product
		actual_product = self.controller.create_product("000000003294", "BC Jazz Apple per kg", 5.93)
		self.assertIsNotNone(actual_product, "product created cannot be null")
		self.assertEqual(expected_product_3, actual_product, "BC Jazz Apple per kg product was created and its data are correct")
		actual_product = self.controller.search_product("000000003294")
		self.assertIsNotNone(actual_product, "product created and retrieved cannot be null")
		self.assertEqual(expected_product_3, actual_product, "third product, BC Jazz Apple per kg, was created, retrieved and its data are correct")

		# creating new products should not affect previous products
		actual_product = self.controller.search_product("629070500083")
		self.assertIsNotNone(actual_product, "product created and retrieved cannot be null, regardless of search order")
		self.assertEqual(expected_product_2, actual_product, "Kicking Horse Coffee product was created, retrieved and its data are correct regardless of search order")
		actual_product = self.controller.search_product("037466022680")
		self.assertIsNotNone(actual_product, "product created and retrieved cannot be null, regardless of search order")
		self.assertEqual(expected_product_1, actual_product, "Lindt Excellence Orange product was created, retrieved and its data are correct regardless of search order")


	def test_retrieve_products(self):
		# some products that will be retrieved
		expected_product_1 = Product("037466022680", "Lindt Excellence Orange", 4.99)
		expected_product_2 = Product("629070500083", "Kicking Horse Coffee", 18.99)
		expected_product_3 = Product("000000003294", "BC Jazz Apple per kg", 5.93)
		expected_product_4 = Product("743434011289", "Lindt Excellence Raspberry", 4.99)
		expected_product_5 = Product("065684112241", "Liberte Strawberry Yogurt", 5.49)

		# cannot do operation without logging in
		with self.assertRaises(IllegalAccessException, msg="cannot retrieve products without logging in"):
			self.controller.retrieve_products("Lindt Excellence Orange")

		# login and create some products
		self.assertTrue(self.controller.login("user", "123456"), "login correctly")
		self.controller.create_product("037466022680", "Lindt Excellence Orange", 4.99)
		self.controller.create_product("629070500083", "Kicking Horse Coffee", 18.99)
		self.controller.create_product("000000003294", "BC Jazz Apple per kg", 5.93)
		self.controller.create_product("743434011289", "Lindt Excellence Raspberry", 4.99)
		self.controller.create_product("065684112241", "Liberte Strawberry Yogurt", 5.49)

		# retrieve one product
		retrieved_list = self.controller.retrieve_products("Kicking Horse Coffee")
		self.assertEqual(1, len(retrieved_list), "retrieved list of products has size 1")
		actual_product = retrieved_list[0]
		self.assertEqual(expected_product_2, actual_product, "retrieved product in the list is Kicking Horse Coffee")

		# retrieve two products
		retrieved_list = self.controller.retrieve_products("Lindt")
		self.assertEqual(2, len(retrieved_list), "retrieved list of products with Lindt keyword has size 2")
		self.assertEqual(expected_product_1, retrieved_list[0], "first product in the retrieved list is Lindt Excellence Orange")
		self.assertEqual(expected_product_4, retrieved_list[1], "second product in the retrieved list is Lindt Excellence Raspberry")

		# retrieve zero products
		retrieved_list = self.controller.retrieve_products("Dove")
		self.assertEqual(0, len(retrieved_list))


	def test_update_product(self):
		# some products that may be updated
		expected_product_1 = Product("037466022680", "Lindt Excellence Orange", 4.99)
		expected_product_2 = Product("629070500083", "Kicking Horse Coffee", 18.99)
		expected_product_3 = Product("000000003294", "BC Jazz Apple per kg", 5.93)
		expected_product_4 = Product("743434011289", "Lindt Excellence Raspberry", 4.99)
		expected_product_5 = Product("065684112241", "Liberte Strawberry Yogurt", 5.49)

		# cannot do operation without logging in
		with self.assertRaises(IllegalAccessException, msg="cannot update product without logging in"):
			self.controller.update_product("037466022680", "037466022680", "Lindt Excellence Orange", 5.49)

		# login
		self.assertTrue(self.controller.login("user", "123456"), "login correctly")

		# try to update a product when there are no products in the system
		with self.assertRaises(IllegalOperationException, msg="cannot update product when there are no products in the system"):
			self.controller.update_product("037466022680", "037466022680", "Lindt Excellence Orange", 5.49)

		# create some products
		self.controller.create_product("037466022680", "Lindt Excellence Orange", 4.99)
		self.controller.create_product("629070500083", "Kicking Horse Coffee", 18.99)
		self.controller.create_product("000000003294", "BC Jazz Apple per kg", 5.93)
		self.controller.create_product("743434011289", "Lindt Excellence Raspberry", 4.99)
		self.controller.create_product("065684112241", "Liberte Strawberry Yogurt", 5.49)

		# update one product, but keep the Product key (UPC) unchanged
		self.assertTrue(self.controller.update_product("037466022680", "037466022680", "Lindt Excellence Orange The Best", 5.49), 
			"update product data and keep the UPC unchanged")
		actual_product = self.controller.search_product("037466022680")
		self.assertNotEqual(expected_product_1, actual_product, "product has updated data, cannot be equal to the original data")
		expected_product_3a = Product("037466022680", "Lindt Excellence Orange The Best", 5.49)
		self.assertEqual(expected_product_3a, actual_product, "product was updated, its data have to be updated and correct")

		# update one product, and change the Product key (UPC) as well
		self.assertTrue(self.controller.update_product("065684112241", "165684112242", "Liberte Strawberry Yogurt New", 5.99), 
			"update product data and also change the UPC")
		actual_product = self.controller.search_product("165684112242")
		self.assertNotEqual(expected_product_5, actual_product, "product has updated data, cannot be equal to the original data")
		expected_product_5a = Product("165684112242", "Liberte Strawberry Yogurt New", 5.99)
		self.assertEqual(expected_product_5a, actual_product, "product was updated, its data have to be updated and correct")

		# update one product with a conflicting existing UPC
		with self.assertRaises(IllegalOperationException, msg="cannot update product and give it a registered UPC"):
			self.controller.update_product("037466022680", "629070500083", "Lindt Excellence Orange The Best", 5.49)


	def test_delete_product(self):
		# some products that may be deleted
		expected_product_1 = Product("037466022680", "Lindt Excellence Orange", 4.99)
		expected_product_2 = Product("629070500083", "Kicking Horse Coffee", 18.99)
		expected_product_3 = Product("000000003294", "BC Jazz Apple per kg", 5.93)
		expected_product_4 = Product("743434011289", "Lindt Excellence Raspberry", 4.99)
		expected_product_5 = Product("065684112241", "Liberte Strawberry Yogurt", 5.49)

		# cannot do operation without logging in
		with self.assertRaises(IllegalAccessException, msg="cannot delete product without logging in"):
			self.controller.delete_product("037466022680")

		# login
		self.assertTrue(self.controller.login("user", "123456"), "login correctly")

		# try to delete a product when there are no products in the system
		with self.assertRaises(IllegalOperationException, msg="cannot delete product when no products are registered"):
			self.controller.delete_product("037466022680")

		# add some products
		self.controller.create_product("037466022680", "Lindt Excellence Orange", 4.99)
		self.controller.create_product("629070500083", "Kicking Horse Coffee", 18.99)
		self.controller.create_product("000000003294", "BC Jazz Apple per kg", 5.93)
		self.controller.create_product("743434011289", "Lindt Excellence Raspberry", 4.99)
		self.controller.create_product("065684112241", "Liberte Strawberry Yogurt", 5.49)

		# delete one product at the start of the collection
		self.assertTrue(self.controller.delete_product("037466022680"), "delete product from the start of the collection")
		self.assertIsNone(self.controller.search_product("037466022680"), "deleted product cannot be found in the system")

		# delete one product at the middle of the collection
		self.assertTrue(self.controller.delete_product("000000003294"), "delete product from the middle of the collection")
		self.assertIsNone(self.controller.search_product("000000003294"), "deleted product cannot be found in the system")

		# delete one product at the end of the collection
		self.assertTrue(self.controller.delete_product("065684112241"), "delete product from the end of the collection")
		self.assertIsNone(self.controller.search_product("065684112241"), "deleted product cannot be found in the system")


	def test_list_products(self):
		# some products that may be listed
		expected_product_1 = Product("037466022680", "Lindt Excellence Orange", 4.99)
		expected_product_2 = Product("629070500083", "Kicking Horse Coffee", 18.99)
		expected_product_3 = Product("000000003294", "BC Jazz Apple per kg", 5.93)
		expected_product_4 = Product("743434011289", "Lindt Excellence Raspberry", 4.99)
		expected_product_5 = Product("065684112241", "Liberte Strawberry Yogurt", 5.49)

		# cannot do operation without logging in
		with self.assertRaises(IllegalAccessException, msg="cannot list products without logging in"):
			self.controller.list_products()

		# login
		self.assertTrue(self.controller.login("user", "123456"), "login correctly")

		# listing products when there are no products in the system
		products_list = self.controller.list_products()
		self.assertEqual(0, len(products_list), "list of products has size 0")

		# add one product
		self.controller.create_product("037466022680", "Lindt Excellence Orange", 4.99)

		# listing products in a singleton list
		products_list = self.controller.list_products()
		self.assertEqual(1, len(products_list), "list of products has size 1")
		self.assertEqual(expected_product_1, products_list[0], "Lindt Excellence Orange product is the only one in the list of products")

		# add some more products
		self.controller.create_product("629070500083", "Kicking Horse Coffee", 18.99)
		self.controller.create_product("000000003294", "BC Jazz Apple per kg", 5.93)
		self.controller.create_product("743434011289", "Lindt Excellence Raspberry", 4.99)
		self.controller.create_product("065684112241", "Liberte Strawberry Yogurt", 5.49)


		# listing products in a larger list
		products_list = self.controller.list_products()
		self.assertEqual(5, len(products_list), "list of products has size 5")
		self.assertEqual(expected_product_1, products_list[0], "product 1 is the first in the list of products")
		self.assertEqual(expected_product_2, products_list[1], "product 2 is the second in the list of products")
		self.assertEqual(expected_product_3, products_list[2], "product 3 is the third in the list of products")
		self.assertEqual(expected_product_4, products_list[3], "product 4 is the fourth in the list of products")
		self.assertEqual(expected_product_5, products_list[4], "product 5 is the fifth in the list of products")

		# deleting some products
		self.controller.delete_product("037466022680")
		self.controller.delete_product("000000003294")
		self.controller.delete_product("065684112241")

		# listing products after deleting some products
		products_list = self.controller.list_products()
		self.assertEqual(2, len(products_list), "list of products has size 2")
		self.assertEqual(expected_product_2, products_list[0], "product 2 is the first in the list of products")
		self.assertEqual(expected_product_4, products_list[1], "product 4 is the second in the list of products")


	def test_search_sale(self):
		# some sales that could be searched
		sale1 = Sale(1, date(2026, 2, 20), 9.98, 0.49, 0.69, 11.16)
		sale2 = Sale(2, date(2026, 2, 20), 18.99, 0.94, 1.32, 21.25)
		sale3 = Sale(3, date(2026, 2, 21), 37.86, 1.89, 2.65, 42.40)
		sale4 = Sale(4, date(2026, 2, 21), 80.79, 4.03, 5.65, 90.47)
		
		# add sales to the sales collection using the add_sale helper method
		# this is not the typical way to add sales, but added here to simplify search tests
		# and to allow the developers to choose their own collection type
		# usually, a sale is initiated, items are recorded, and then the sale is finished
		self.controller.add_sale(sale1)
		self.controller.add_sale(sale2)
		self.controller.add_sale(sale3)
		self.controller.add_sale(sale4)

		# cannot do operation without logging in
		with self.assertRaises(IllegalAccessException, msg="cannot search sale without logging in"):
			self.controller.search_sale(1)

		# login
		self.assertTrue(self.controller.login("user", "123456"), "login correctly")

		# search an inexistent sale
		self.assertIsNone(self.controller.search_sale(23), "searching inexistent sale returns None")

		# search existing sales
		self.assertEqual(sale1, self.controller.search_sale(1), "searching returns sale 1")
		self.assertEqual(sale2, self.controller.search_sale(2), "searching returns sale 2")
		self.assertEqual(sale4, self.controller.search_sale(4), "searching returns sale 4")


	def test_list_sales(self):
		# some sales that could be listed
		expected_sale1 = Sale(1, date(2026, 2, 20), 9.98, 0.49, 0.69, 11.16)
		expected_sale2 = Sale(2, date(2026, 2, 20), 18.99, 0.94, 1.32, 21.25)
		expected_sale3 = Sale(3, date(2026, 2, 21), 37.86, 1.89, 2.65, 42.40)
		expected_sale4 = Sale(4, date(2026, 2, 21), 80.79, 4.03, 5.65, 90.47)
		expected_sale5 = Sale(5, date(2026, 2, 23), 80.79, 4.03, 5.65, 90.47)
		
		# cannot do operation without logging in
		with self.assertRaises(IllegalAccessException, msg="cannot list sales without logging in"):
			self.controller.list_sales()

		# login
		self.assertTrue(self.controller.login("user", "123456"), "login correctly")

		# inexistent sales lead to an empty sales list
		actual_sales_list = self.controller.list_sales()
		self.assertEqual(0, len(actual_sales_list), "list of sales has size 0")

		# add sales to the sales collection using the add_sale helper method
		# this is not the typical way to add sales, but added here to simplify search tests
		# and to allow the developers to choose their own collection type
		# usually, a sale is usually initiated, items are recorded, and then the sale is finished
		self.controller.add_sale(expected_sale1)

		# one sale leads to a singleton sales list
		actual_sales_list = self.controller.list_sales()
		self.assertEqual(1, len(actual_sales_list), "list of sales has size 1")
		self.assertEqual(expected_sale1, actual_sales_list[0], "expected sale 1 is the only one in the list of sales")

		# add two more sales, which leads to a list with 3 sales
		self.controller.add_sale(expected_sale2)
		self.controller.add_sale(expected_sale3)
		actual_sales_list = self.controller.list_sales()
		self.assertEqual(3, len(actual_sales_list), "list of sales has size 1")
		self.assertEqual(expected_sale1, actual_sales_list[0], "expected sale 1 is the first in the list of sales")
		self.assertEqual(expected_sale2, actual_sales_list[1], "expected sale 2 is the second in the list of sales")
		self.assertEqual(expected_sale3, actual_sales_list[2], "expected sale 3 is the third in the list of sales")

		# add yet two more sales, which leads to a list with 5 sales
		self.controller.add_sale(expected_sale4)
		self.controller.add_sale(expected_sale5)
		actual_sales_list = self.controller.list_sales()
		self.assertEqual(5, len(actual_sales_list), "list of sales has size 1")
		self.assertEqual(expected_sale1, actual_sales_list[0], "expected sale 1 is the first in the list of sales")
		self.assertEqual(expected_sale2, actual_sales_list[1], "expected sale 2 is the second in the list of sales")
		self.assertEqual(expected_sale3, actual_sales_list[2], "expected sale 3 is the third in the list of sales")
		self.assertEqual(expected_sale4, actual_sales_list[3], "expected sale 4 is the fourth in the list of sales")
		self.assertEqual(expected_sale5, actual_sales_list[4], "expected sale 5 is the fifth in the list of sales")


	def test_initiate_sale(self):
		# expected initiated sale must have zero values and no id or date
		expected_initiated_sale = Sale(None, None, 0.00, 0.00, 0.00, 0.00)

		# cannot do operation without logging in
		with self.assertRaises(IllegalAccessException, msg="cannot initiate sale without logging in"):
			self.controller.initiate_sale()

		# login
		self.assertTrue(self.controller.login("user", "123456"), "login correctly")

		# initiate sale correctly
		self.assertTrue(self.controller.initiate_sale(), "sale initiated")
		self.assertEqual(expected_initiated_sale, self.controller.get_current_sale(), "initiated sale must be have zero values and no id or date")
		
		# cannot initiate sale if there is a current sale in progress
		with self.assertRaises(IllegalOperationException, msg="cannot initiate sale with a sale in progress"):
			self.controller.initiate_sale()


	def test_cancel_current_sale(self):
		# cannot do operation without logging in
		with self.assertRaises(IllegalAccessException, msg="cannot cancel sale without logging in"):
			self.controller.cancel_current_sale()

		# login
		self.assertTrue(self.controller.login("user", "123456"), "login correctly")

		# cannot cancel sale without initiating it first
		with self.assertRaises(NoCurrentSaleException, msg="cannot cancel sale without initiating it first"):
			self.controller.cancel_current_sale()

		# initiate sale correctly
		self.assertTrue(self.controller.initiate_sale(), "sale initiated")
		self.assertIsNotNone(self.controller.get_current_sale(), "initiated sale is valid")

		# cancel sale
		self.controller.cancel_current_sale()
		self.assertIsNone(self.controller.get_current_sale(), "there must be no current sale after cancelling")


	def test_add_new_sale_line_item(self):
		# some sale line items that may be created
		expected_sale_line_item_1 = SaleLineItem(1, 2, 4.99, "037466022680")
		expected_sale_line_item_2 = SaleLineItem(2, 1, 18.99, "629070500083")
		expected_sale_line_item_3 = SaleLineItem(3, 1.5, 5.93, "000000003294")

		# cannot do operation without logging in
		with self.assertRaises(IllegalAccessException, msg="cannot add new sale line item without logging in"):
			self.controller.add_new_sale_line_item(2, "037466022680")

		# login
		self.assertTrue(self.controller.login("user", "123456"), "login correctly")

		# cannot do operation without a valid current sale
		with self.assertRaises(NoCurrentSaleException, msg="cannot add sale new line item without a valid current sale"):
			self.controller.add_new_sale_line_item(2, "037466022680")

		# initiate sale
		self.controller.initiate_sale()

		# cannot add a new line item if the product is not registered in the system
		with self.assertRaises(InvalidProductException, msg="cannot add sale new line item with an inexisting product"):
			self.controller.add_new_sale_line_item(2, "037466022680")

		# add new line item successfully
		self.controller.create_product("037466022680", "Lindt Excellence Orange", 4.99)
		actual_sale_line_item = self.controller.add_new_sale_line_item(2, "037466022680")
		self.assertEqual(1, self.controller.get_current_sale().get_number_sale_line_items(), "added one sale line item to the current sale")
		self.assertEqual(expected_sale_line_item_1, actual_sale_line_item, "actual sale line item must be sale line item 1")

		# add a two more new line items successfully
		self.controller.create_product("629070500083", "Kicking Horse Coffee", 18.99)
		self.controller.create_product("000000003294", "BC Jazz Apple per kg", 5.93)
		actual_sale_line_item = self.controller.add_new_sale_line_item(1, "629070500083")
		self.assertEqual(2, self.controller.get_current_sale().get_number_sale_line_items(), "added one sale line item to the current sale")
		self.assertEqual(expected_sale_line_item_2, actual_sale_line_item, "actual sale line item must be sale line item 1")
		actual_sale_line_item = self.controller.add_new_sale_line_item(1.5, "000000003294")
		self.assertEqual(3, self.controller.get_current_sale().get_number_sale_line_items(), "added one sale line item to the current sale")
		self.assertEqual(expected_sale_line_item_3, actual_sale_line_item, "actual sale line item must be sale line item 1")


	def test_finish_current_sale(self):
		# some sale line items that may be created
		expected_sale_1 = Sale(1, datetime.now().date(), 9.98, 0.50, 0.70, 11.18)
		expected_sale_2 = Sale(2, datetime.now().date(), 18.99, 0.95, 1.33, 21.27)
		expected_sale_3 = Sale(3, datetime.now().date(), 37.86, 1.89, 2.65, 42.40)

		# cannot do operation without logging in
		with self.assertRaises(IllegalAccessException, msg="cannot finish current sale without logging in"):
			self.controller.finish_current_sale()

		# login
		self.assertTrue(self.controller.login("user", "123456"), "login correctly")

		# add some products to the system
		self.controller.create_product("037466022680", "Lindt Excellence Orange", 4.99)
		self.controller.create_product("629070500083", "Kicking Horse Coffee", 18.99)
		self.controller.create_product("000000003294", "BC Jazz Apple per kg", 5.93)

		# cannot do operation without a valid current sale
		with self.assertRaises(NoCurrentSaleException, msg="cannot finish sale without a valid current sale"):
			self.controller.finish_current_sale()

		# initiate first sale
		self.controller.initiate_sale()

		# cannot finish sale with no sale line items
		with self.assertRaises(IllegalOperationException, msg="cannot finish current sale without adding at least one sale line item"):
			self.controller.finish_current_sale()

		# finish first sale after adding one new line item
		self.controller.add_new_sale_line_item(2, "037466022680")
		actual_sale = self.controller.finish_current_sale()
		self.assertIsNotNone(actual_sale)
		self.assertEqual(expected_sale_1, actual_sale, "sale 1 with one sale line item must be correct")
		self.assertEqual(1, self.controller.get_number_sales())

		# initiate second sale
		self.controller.initiate_sale()

		# finish second sale after adding one new line item
		self.controller.add_new_sale_line_item(1, "629070500083")
		actual_sale = self.controller.finish_current_sale()
		self.assertIsNotNone(actual_sale)
		self.assertEqual(expected_sale_2, actual_sale, "sale 2 with one sale line item must be correct")
		self.assertEqual(2, self.controller.get_number_sales())

		# initiate third sale
		self.controller.initiate_sale()

		# finish third sale after adding three new line items
		self.controller.add_new_sale_line_item(2, "037466022680")
		self.controller.add_new_sale_line_item(1, "629070500083")
		self.controller.add_new_sale_line_item(1.5, "000000003294")
		actual_sale = self.controller.finish_current_sale()
		self.assertIsNotNone(actual_sale)
		self.assertEqual(expected_sale_3, actual_sale, "sale 3 with three sale line items must be correct")
		self.assertEqual(3, self.controller.get_number_sales())


	def test_print_sale_receipt(self):
		# some receipts that may be printed
		expected_receipt_1 = \
'''MARKET AT VICTORIA - SALES RECEIPT

Sale # 1

-----------------------------------------------------------
ITEM NAME                      -    QTY x   UNIT - SUBTOTAL

Lindt Excellence Orange        -   2.00 x   4.99 -   9.98
-----------------------------------------------------------
NET SALE                                         -   9.98
GST (5%)                                         -   0.50
PST (7%)                                         -   0.70
-----------------------------------------------------------
TOTAL SALE                                       -  11.18
'''
		expected_receipt_2 = \
'''MARKET AT VICTORIA - SALES RECEIPT

Sale # 2

-----------------------------------------------------------
ITEM NAME                      -    QTY x   UNIT - SUBTOTAL

Kicking Horse Coffee           -   1.00 x  18.99 -  18.99
-----------------------------------------------------------
NET SALE                                         -  18.99
GST (5%)                                         -   0.95
PST (7%)                                         -   1.33
-----------------------------------------------------------
TOTAL SALE                                       -  21.27
'''
		expected_receipt_3 = \
'''MARKET AT VICTORIA - SALES RECEIPT

Sale # 3

-----------------------------------------------------------
ITEM NAME                      -    QTY x   UNIT - SUBTOTAL

Lindt Excellence Orange        -   2.00 x   4.99 -   9.98
Kicking Horse Coffee           -   1.00 x  18.99 -  18.99
BC Jazz Apple per kg           -   1.50 x   5.93 -   8.89
-----------------------------------------------------------
NET SALE                                         -  37.86
GST (5%)                                         -   1.89
PST (7%)                                         -   2.65
-----------------------------------------------------------
TOTAL SALE                                       -  42.40
'''
		# cannot do operation without logging in
		with self.assertRaises(IllegalAccessException, msg="cannot print sale receipt without logging in"):
			self.controller.print_sale_receipt()

		# login
		self.assertTrue(self.controller.login("user", "123456"), "login correctly")

		# add some products to the system
		self.controller.create_product("037466022680", "Lindt Excellence Orange", 4.99)
		self.controller.create_product("629070500083", "Kicking Horse Coffee", 18.99)
		self.controller.create_product("000000003294", "BC Jazz Apple per kg", 5.93)

		# cannot do operation without a valid current sale
		with self.assertRaises(NoCurrentSaleException, msg="cannot print sale receipt without a valid current sale"):
			self.controller.print_sale_receipt()

		# initiate first sale
		self.controller.initiate_sale()

		# cannot print sale receipt with no sale line items
		self.assertIsNone(self.controller.print_sale_receipt(), "cannot print sale receipt without adding at least one sale line item")

		# finish first sale after adding one new line item
		self.controller.add_new_sale_line_item(2, "037466022680")
		actual_sale = self.controller.finish_current_sale() # print sale receipt is done inside finish current sale
		actual_receipt = actual_sale.get_sale_receipt()
		self.assertIsNotNone(actual_receipt)
		self.assertEqual(expected_receipt_1, actual_receipt, "sale 1 receipt with one sale line item must be correct")

		# initiate second sale
		self.controller.initiate_sale()

		# finish second sale after adding one new line item
		self.controller.add_new_sale_line_item(1, "629070500083")
		actual_sale = self.controller.finish_current_sale() # print sale receipt is done inside finish current sale
		actual_receipt = actual_sale.get_sale_receipt()
		self.assertIsNotNone(actual_receipt)
		self.assertEqual(expected_receipt_2, actual_receipt, "sale 2 receipt with one sale line item must be correct")

		# initiate third sale
		self.controller.initiate_sale()

		# finish third sale after adding three new line items
		self.controller.add_new_sale_line_item(2, "037466022680")
		self.controller.add_new_sale_line_item(1, "629070500083")
		self.controller.add_new_sale_line_item(1.5, "000000003294")
		actual_sale = self.controller.finish_current_sale() # print sale receipt is done inside finish current sale
		actual_receipt = actual_sale.get_sale_receipt()
		self.assertIsNotNone(actual_receipt)
		self.assertEqual(expected_receipt_3, actual_receipt, "sale 3 receipt with three sale line items must be correct")


	def test_create_sale_line_item(self):
		# some sale line items that may be created
		expected_sale_line_item_1 = SaleLineItem(1, 2, 4.99, "037466022680")
		expected_sale_line_item_2 = SaleLineItem(2, 1, 18.99, "629070500083")
		expected_sale_line_item_3 = SaleLineItem(3, 1.5, 5.93, "000000003294")

		# cannot do operation without logging in
		with self.assertRaises(IllegalAccessException, msg="cannot add sale line item without logging in"):
			self.controller.create_sale_line_item(2, 4.99, "037466022680")

		# login
		self.assertTrue(self.controller.login("user", "123456"), "login correctly")

		# cannot do operation without a valid current sale
		with self.assertRaises(NoCurrentSaleException, msg="cannot search sale line item without a valid current sale"):
			self.controller.search_sale_line_item(1)
		with self.assertRaises(NoCurrentSaleException, msg="cannot create sale line item without a valid current sale"):
			self.controller.create_sale_line_item(2, 4.99, "037466022680")

		# initiate sale
		self.controller.initiate_sale()

		# add one sale line item
		actual_sale_line_item = self.controller.create_sale_line_item(2, 4.99, "037466022680")
		self.assertIsNotNone(actual_sale_line_item, "sale line item 1 was created and is valid")

		# implement __eq__(self, other) in Post to compare sale line items based on their code, title and text
		self.assertEqual(expected_sale_line_item_1, actual_sale_line_item, "sale line item 1 was created and its data are correct")

		# after creating the sale line item, one should be able to search it
		actual_sale_line_item = self.controller.search_sale_line_item(1)
		self.assertIsNotNone(actual_sale_line_item, "sale line item created and retrieved cannot be null")
		self.assertEqual(expected_sale_line_item_1, actual_sale_line_item, "sale line item 1 was created, retrieved and its data are correct")

		# add a second sale line item
		actual_sale_line_item = self.controller.create_sale_line_item(1, 18.99, "629070500083")
		self.assertIsNotNone(actual_sale_line_item, "sale line item 2 was created and is valid")
		self.assertEqual(expected_sale_line_item_2, actual_sale_line_item, "sale line item 2 was created and its data are correct")

		# after creating the sale line item, one should be able to search it
		actual_sale_line_item = self.controller.search_sale_line_item(2)
		self.assertIsNotNone(actual_sale_line_item, "sale line item created and retrieved cannot be null")
		self.assertEqual(expected_sale_line_item_2, actual_sale_line_item, "sale line item 2 was created, retrieved and its data are correct")

		# add a third sale line item
		actual_sale_line_item = self.controller.create_sale_line_item(1.5, 5.93, "000000003294")
		self.assertIsNotNone(actual_sale_line_item, "sale line item 3 was created and is valid")
		self.assertEqual(expected_sale_line_item_3, actual_sale_line_item, "sale line item 3 was created and its data are correct")

		# after creating the sale line item, one should be able to search it
		actual_sale_line_item = self.controller.search_sale_line_item(3)
		self.assertIsNotNone(actual_sale_line_item, "sale line item created and retrieved cannot be null")
		self.assertEqual(expected_sale_line_item_3, actual_sale_line_item, "sale line item 3 was created, retrieved and its data are correct")

		# creating new sale line items should not affect previous sale line items
		actual_sale_line_item = self.controller.search_sale_line_item(2)
		self.assertIsNotNone(actual_sale_line_item, "sale line item created and retrieved cannot be null regardless of search order")
		self.assertEqual(expected_sale_line_item_2, actual_sale_line_item, "sale line item 2 was created, retrieved and its data are correct regardless of search order")
		actual_sale_line_item = self.controller.search_sale_line_item(1)
		self.assertIsNotNone(actual_sale_line_item, "sale line item created and retrieved cannot be null regardless of search order")
		self.assertEqual(expected_sale_line_item_1, actual_sale_line_item, "sale line item 1 was created, retrieved and its data are correct regardless of search order")


	def test_print_sale_line_item(self):
		# some sale line items that may be printed
		expected_sale_line_item_1_print = "Lindt Excellence Orange        -   2.00 x   4.99 -   9.98\n"
		expected_sale_line_item_2_print = "Kicking Horse Coffee           -   1.00 x  18.99 -  18.99\n"
		expected_sale_line_item_3_print = "BC Jazz Apple per kg           -   1.50 x   5.93 -   8.89\n"

		# cannot do operation without logging in
		with self.assertRaises(IllegalAccessException, msg="cannot list a sale line item for a sale without logging in"):
			self.controller.print_sale_line_item(1)

		# login
		self.assertTrue(self.controller.login("user", "123456"), "login correctly")

		# cannot do operation without a valid current sale
		with self.assertRaises(NoCurrentSaleException, msg="cannot list a sale line item with no valid current sale"):
			self.controller.print_sale_line_item(1)

		# add some products to the system
		self.controller.create_product("037466022680", "Lindt Excellence Orange", 4.99)
		self.controller.create_product("629070500083", "Kicking Horse Coffee", 18.99)
		self.controller.create_product("000000003294", "BC Jazz Apple per kg", 5.93)

		# initiate sale
		self.controller.initiate_sale()

		# listing a sale line item when the current sale has no sale line items
		sale_line_item = self.controller.print_sale_line_item(1)
		self.assertIsNone(sale_line_item, "sale line item cannot be recovered since it was not added to the sale")

		# listing a sale line item from a singleton list
		self.controller.add_new_sale_line_item(2, "037466022680")
		sale_line_item_print = self.controller.print_sale_line_item(1)
		self.assertEqual(expected_sale_line_item_1_print, sale_line_item_print, "sale line item 1 is the printed sale line item.")

		# add some more sale line items
		self.controller.add_new_sale_line_item(1, "629070500083")
		self.controller.add_new_sale_line_item(1.5, "000000003294")

		# listing a sale line item from a larger list
		sale_line_item_print = self.controller.print_sale_line_item(3)
		self.assertEqual(expected_sale_line_item_3_print, sale_line_item_print, "sale line item 3 is the printed sale line item.")

		sale_line_item_print = self.controller.print_sale_line_item(2)
		self.assertEqual(expected_sale_line_item_2_print, sale_line_item_print, "sale line item 2 is the printed sale line item.")


	def test_print_sale_line_items(self):
		# some sale line items that may be printed
		expected_sale_line_item_1_print = "Lindt Excellence Orange        -   2.00 x   4.99 -   9.98\n"
		expected_sale_line_item_2_print = "Kicking Horse Coffee           -   1.00 x  18.99 -  18.99\n"
		expected_sale_line_item_3_print = "BC Jazz Apple per kg           -   1.50 x   5.93 -   8.89\n"
		expected_sale_line_item_4_print = "Lindt Excellence Raspberry     -   3.00 x   4.99 -  14.97\n"
		expected_sale_line_item_5_print = "Liberte Strawberry Yogurt      -   4.00 x   5.49 -  21.96\n"

		# cannot do operation without logging in
		with self.assertRaises(IllegalAccessException, msg="cannot list sale line items without logging in"):
			self.controller.print_sale_line_items()

		# login
		self.assertTrue(self.controller.login("user", "123456"), "login correctly")

		# cannot do operation without a valid current sale
		with self.assertRaises(NoCurrentSaleException, msg="cannot list sale line items when there is no current sale"):
			self.controller.print_sale_line_items()

		# add some products to the system
		self.controller.create_product("037466022680", "Lindt Excellence Orange", 4.99)
		self.controller.create_product("629070500083", "Kicking Horse Coffee", 18.99)
		self.controller.create_product("000000003294", "BC Jazz Apple per kg", 5.93)
		self.controller.create_product("743434011289", "Lindt Excellence Raspberry", 4.99)
		self.controller.create_product("065684112241", "Liberte Strawberry Yogurt", 5.49)

		# initiate sale
		self.controller.initiate_sale()

		# listing sale line items when the current sale has no sale line items
		actual_print = self.controller.print_sale_line_items()
		self.assertIsNone(actual_print, "No sale line items in the current sale.")

		# listing sale line items in a singleton list
		self.controller.add_new_sale_line_item(2, "037466022680")
		expected_print = expected_sale_line_item_1_print
		actual_print = self.controller.print_sale_line_items()
		self.assertEqual(expected_print, actual_print, "sale line item 1 is the listed sale line item.")

		# add two more sale line items
		self.controller.add_new_sale_line_item(1, "629070500083")
		self.controller.add_new_sale_line_item(1.5, "000000003294")

		# listing sale line items in a larger list
		expected_print = expected_sale_line_item_1_print + expected_sale_line_item_2_print + expected_sale_line_item_3_print
		actual_print = self.controller.print_sale_line_items()
		self.assertEqual(expected_print, actual_print, "sale line item 1 is the listed sale line item.")

		# add two more sale line items
		self.controller.add_new_sale_line_item(3, "743434011289")
		self.controller.add_new_sale_line_item(4, "065684112241")

		# listing sale line items in a larger list
		expected_print = expected_sale_line_item_1_print + expected_sale_line_item_2_print + expected_sale_line_item_3_print + expected_sale_line_item_4_print + expected_sale_line_item_5_print
		actual_print = self.controller.print_sale_line_items()
		self.assertEqual(expected_print, actual_print, "sale line item 1 is the listed sale line item.")

if __name__ == '__main__':
	unittest.main()