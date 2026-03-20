from abc import ABC, abstractmethod
class ProductDAO(ABC):
    @abstractmethod
    def search_product(self, key):
        pass
    @abstractmethod
    def create_product(self, product):
        pass
    @abstractmethod
    def retrieve_products(self, search_string):
        pass
    @abstractmethod
    def update_product(self, key, product):
        pass
    @abstractmethod
    def delete_product(self, key):
        pass
    @abstractmethod
    def list_products(self):
        pass

