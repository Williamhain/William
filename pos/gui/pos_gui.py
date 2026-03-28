import sys
from pos.configuration import Configuration
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow

class PosGUI(QMainWindow):

    def __init__(self):
        super().__init__()
        # set autosave to True to ensure persistence is working
        self.configuration = Configuration()
        self.configuration.__class__.autosave = True
        # Continue here with your code!



def main():
    app = QApplication(sys.argv)
    window = PosGUI()
    window.show()
    app.exec()

if __name__ == '__main__':
    main()
