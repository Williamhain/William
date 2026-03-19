from unittest import TestCase
from unittest import main
from pos.product import Product
import datetime

class ProductTest(TestCase):
	
	def setUp(self):
		self.product = Product("037466022680", "Lindt Excellence Orange", 4.99)

	def test_eq(self):
		same_product = Product("037466022680", "Lindt Excellence Orange", 4.99)
		different_product_1 = Product("629070500083", "Kicking Horse Coffee", 18.99)
		different_product_2 = Product("629070500083", "Lindt Excellence Orange", 4.99)
		different_product_3 = Product("037466022680", "Kicking Horse Coffee", 4.99)
		self.assertTrue(self.product == self.product)
		self.assertTrue(self.product == same_product)
		self.assertFalse(self.product == different_product_1)
		self.assertFalse(self.product == different_product_2)
		self.assertFalse(self.product == different_product_3)

	def test_str(self):
		same_product = Product("037466022680", "Lindt Excellence Orange", 4.99)
		different_product_1 = Product("629070500083", "Kicking Horse Coffee", 18.99)
		different_product_2 = Product("629070500083", "Lindt Excellence Orange", 4.99)
		different_product_3 = Product("037466022680", "Kicking Horse Coffee", 4.99)
		self.assertEqual("037466022680; Lindt Excellence Orange; 4.99", str(self.product))
		self.assertEqual("037466022680; Lindt Excellence Orange; 4.99", str(same_product))
		self.assertEqual("629070500083; Kicking Horse Coffee; 18.99", str(different_product_1))
		self.assertEqual("629070500083; Lindt Excellence Orange; 4.99", str(different_product_2))
		self.assertEqual("037466022680; Kicking Horse Coffee; 4.99", str(different_product_3))
		self.assertEqual(str(same_product), str(self.product))
		self.assertNotEqual(str(different_product_1), str(self.product))
		self.assertNotEqual(str(different_product_2), str(self.product))
		self.assertNotEqual(str(different_product_3), str(self.product))

	def test_repr(self):
		same_product = Product("037466022680", "Lindt Excellence Orange", 4.99)
		different_product_1 = Product("629070500083", "Kicking Horse Coffee", 18.99)
		different_product_2 = Product("629070500083", "Lindt Excellence Orange", 4.99)
		different_product_3 = Product("037466022680", "Kicking Horse Coffee", 4.99)
		self.assertEqual("Product('037466022680', 'Lindt Excellence Orange', 4.99)", repr(self.product))
		self.assertEqual("Product('037466022680', 'Lindt Excellence Orange', 4.99)", repr(same_product))
		self.assertEqual("Product('629070500083', 'Kicking Horse Coffee', 18.99)", repr(different_product_1))
		self.assertEqual("Product('629070500083', 'Lindt Excellence Orange', 4.99)", repr(different_product_2))
		self.assertEqual("Product('037466022680', 'Kicking Horse Coffee', 4.99)", repr(different_product_3))
		self.assertEqual(repr(same_product), repr(self.product))
		self.assertNotEqual(repr(different_product_1), repr(self.product))
		self.assertNotEqual(repr(different_product_2), repr(self.product))
		self.assertNotEqual(repr(different_product_3), repr(self.product))


if __name__ == '__main__':
	unittest.main()