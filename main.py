from PyQt5.QtWidgets import QLabel, QLineEdit, QComboBox, QPushButton, QMessageBox, QWidget, QApplication
from PyQt5.QtGui import QIntValidator
from filters import Filters
from parsers import WebParsing
import sys


class Window(QWidget):
    def __init__(self, parent=None):
        """
        :param parent: PyQT5
        """
        super(Window, self).__init__(parent)

        # model menu
        self.my_menu = Filters('de')

        # this for page
        self.country = ''
        self.page = 0
        self.limit = 1

        # this for category search
        self.type = 0
        self.category = 0

        # QT elements
        self.top = 100
        self.left = 100
        self.width = 400
        self.height = 300

        self.create_q_label_country()
        self.q_country = self.create_q_input_country()

        self.create_q_label_start_page()
        self.q_start_page = self.crete_q_input_start_page()

        self.create_q_label_limit()
        self.q_limit = self.create_q_input_limit()

        self.create_q_label_category()
        self.q_select_category = self.create_q_select_category()

        self.create_q_label_type()
        self.q_select_type = self.create_q_select_type()

        self.q_button = self.create_q_button()

        self.create_q_window()

    def create_q_window(self):
        """
        :return: -
        """
        self.setWindowTitle("Downloading image from avto-nomer.ru")
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.show()

    def create_q_label_country(self):
        """
        :return: -
        """
        label = QLabel("Country", self)
        label.setText("Country *")
        label.move(2, 0)

    def create_q_input_country(self):
        """
        :return: -
        """
        country = QLineEdit(self)
        country.setGeometry(2, 17, 395, 25)
        country.setText("de")
        country.textChanged.connect(self.change_country_text)
        return country

    def create_q_label_start_page(self):
        """
        :return: -
        """
        label = QLabel("Start Page", self)
        label.setText("Start Page (0 - 9999)")
        label.move(2, 45)

    def crete_q_input_start_page(self):
        """
        :return: -
        """
        start_page = QLineEdit(self)
        start_page.setGeometry(2, 62, 395, 25)
        start_page.setValidator(QIntValidator(0, 9999))
        return start_page

    def create_q_label_limit(self):
        """
        :return: -
        """
        label = QLabel("Limit", self)
        label.setText("Limit (1 - 999)")
        label.move(2, 90)

    def create_q_input_limit(self):
        """
        :return: -
        """
        limit = QLineEdit(self)
        limit.setGeometry(2, 107, 395, 25)
        limit.setValidator(QIntValidator(1, 999))
        return limit

    def create_q_label_category(self):
        """
        :return: -
        """
        label = QLabel("Category", self)
        label.setText("Category")
        label.move(2, 135)

    def create_q_select_category(self):
        """
        :return: -
        """
        category = QComboBox(self)
        category.setGeometry(2, 155, 395, 25)
        category.addItems(
            self.my_menu.get_category_dict().keys()
        )

        return category

    def create_q_label_type(self):
        """
        :return: -
        """
        label = QLabel("Type", self)
        label.setText("Type")
        label.move(2, 183)

    def create_q_select_type(self):
        """
        :return: -
        """
        type = QComboBox(self)
        type.setGeometry(2, 200, 395, 25)
        type.addItems(
            self.my_menu.get_type_dict().keys()
        )

        return type

    def create_q_button(self):
        """
        :return: -
        """
        button = QPushButton("Download", self)
        button.setGeometry(158, 250, 75, 25)
        button.clicked.connect(self.click_button)
        return button

    def create_q_message_box(self, text):
        """
        :param text: str
        :return: -
        """
        message_box = QMessageBox(self)
        message_box.setText(text)
        message_box.exec()

    def change_country_text(self):
        """
        :return: -
        """
        country = self.q_country.text()
        if len(country) > 1:
            self.my_menu = Filters(country)

            self.q_select_category.clear()
            self.q_select_category.addItems(self.my_menu.get_category_dict().keys())
            self.q_select_category.update()

            self.q_select_type.clear()
            self.q_select_type.addItems(self.my_menu.get_type_dict().keys())
            self.q_select_type.update()

    def click_button(self):
        """
        :return: -
        """
        # input text
        country = self.q_country.text()
        start_page = self.q_start_page.text()
        limit = self.q_limit.text()
        # select
        category = self.q_select_category.currentText()
        type = self.q_select_type.currentText()
        # dict
        category_dict = self.my_menu.get_category_dict()

        type_dict = self.my_menu.get_type_dict()

        if len(country) > 0:
            self.country = country
        if len(start_page) > 0:
            self.page = int(start_page)
        if len(limit) > 0:
            self.limit = int(limit)
        if len(category_dict) > 0 and len(type_dict) > 0:
            self.category = category_dict[category]
            self.type = type_dict[type]

            model = WebParsing(country=self.country, page=self.page, limit=self.limit, category=self.category,
                               type=self.type)
            model.parse_general_page()
            model.parse_image_page()
            model.get_images()
            model.create_csv()

            print("Finish Downloading ...")

        else:
            print("There is no page to download ...")
            self.create_q_message_box("There is no page to download ...")


if __name__ == '__main__':  #

    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())
