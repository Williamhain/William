from PyQt6 import QtCore
from PyQt6.QtCore import Qt

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