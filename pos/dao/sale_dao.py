from abc import ABC, abstractmethod
class SaleDAO(ABC):
    @abstractmethod
    def search_sale(self, key):
        pass
    @abstractmethod
    def create_sale(self, sale):
        pass
    @abstractmethod
    def list_sales(self):
        pass

