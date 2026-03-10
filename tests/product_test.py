# product_test.py
import unittest
from pos.product import Product

class ProductTest(unittest.TestCase):

    def setUp(self):
        #create some products as examples to use for multiple tests
        self.product1 = Product("037466022680", "Lindt Excellence Orange", 4.99)
        self.product2 = Product("037466022680", "Lindt Excellence Orange", 4.99)
        self.product3 = Product("629070500083", "Kicking Horse Coffee", 18.99)

    def test_initialization(self):
        #verify that the constructor assigns attributes properly
        self.assertEqual(self.product1.upc, "037466022680", "UPC should match the initialized value")
        self.assertEqual(self.product1.product_name, "Lindt Excellence Orange", "Product name should match")
        self.assertEqual(self.product1.price, 4.99, "Price should match")

    def test_equality(self):
        #verify that two separate products with the same data are equal
        self.assertTrue(self.product1 == self.product2, "Products with identical data should be equal")
        
        #verify that products with different data are not equal
        self.assertFalse(self.product1 == self.product3, "Products with different data should not be equal")

if __name__ == '__main__':
    unittest.main()