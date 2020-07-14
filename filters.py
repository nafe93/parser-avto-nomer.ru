import os
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup


class Filters:
    def __init__(self, country):
        """
        :param country: str
        """
        self.url = "https://avto-nomer.ru/" + country + "/search"
        self.html = self.get_menu()

    def get_menu(self):
        """
        :return: bs4
        """
        try:
            html = requests.get(self.url).content
            return html
        except:
            print("Bad connect, please check your internet connection or website url ...")
            exit()

    def get_category_dict(self):
        """
        :return: dict
        """
        category_dict = {}
        code = requests.get(self.url).status_code

        if code == 200:
            soup = BeautifulSoup(self.html, 'html.parser')
            ctype = soup.find("select", {"name": "ctype"})
            if ctype:

                options = ctype.find_all("option")

                if options:

                    for option in options:
                        option_value = option['value']
                        option_text = option.text

                        if len(option_value) == 0:
                            option_value = 0

                        category_dict[option_text] = option_value

        return category_dict

    def get_type_dict(self):
        """
        :return: dict
        """
        type_dict = {}
        code = requests.get(self.url).status_code

        if code == 200:
            soup = BeautifulSoup(self.html, 'html.parser')
            ctype = soup.find("select", {"name": "fon"})

            if ctype:

                options = ctype.find_all("option")

                if options:

                    for option in options:
                        option_value = option['value']
                        option_text = option.text

                        if len(option_value) == 0:
                            option_value = 0

                        type_dict[option_text] = option_value

        return type_dict
