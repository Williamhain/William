import sys
from pos.configuration import Configuration
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QWidget, QStackedLayout, QVBoxLayout
from pos.controller import Controller
from pos.exception.invalid_logout_exception import InvalidLogoutException
from pos.exception.invalid_login_exception import InvalidLoginException

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
        layout = QVBoxLayout()
        layout.addWidget(self.main_message_label)
        layout.addWidget(self.logout_button)

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


def main():
    app = QApplication(sys.argv)
    window = PosGUI()
    window.show()
    app.exec()

if __name__ == '__main__':
    main()
