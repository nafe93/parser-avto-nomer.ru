import os
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from Selenium import Chrome
from datetime import datetime


class WebParsing:
    """
    url - string
    country  - string
    category - int
    type     - int
    page     - int
    key - string for search
    limit - int limit download
    """

    def __init__(self, url='https://avto-nomer.ru/', country='de', category=0, type=0, page=0,
                 key='nomer', limit=1):
        self.url = url
        self.country = country
        self.category = category
        self.limit = limit
        self.type = type
        self.page = page
        self.key = self.country + '/' + key
        self.links_to_download = []
        self.csv = []

    def _request(self, url):
        try:
            html = requests.get(url).content
            return html
        except:
            print("Bad connect, please check your internet connection or website url ...")
            exit()

    def _get_text(self):
        if len(self.url) == 0:
            print("Please input url")
            exit()
        if len(self.country) == 0:
            print("Please input country")
            exit()

        url = self.url + '/' + self.country + '/' + 'gallery.php?'

        if self.category > 0:
            url += 'ctype=' + str(self.category) + '&'
        if self.type > 0:
            url += 'fon=' + str(self.type) + '&'
        if self.page > 0:
            url += 'start=' + str(self.page) + '&'

        html = self._request(url)
        return html

    def parser_general_page(self):
        cars_links = []

        for i in range(self.page, self.page + self.limit):

            self.page = i
            html = self._get_text()
            soup = BeautifulSoup(html, 'html.parser')

            if soup is not None:
                for div in soup.find_all("div", {"class": "col-md-9"}):
                    print(f"Parsing general page number {self.page} is started ...")
                    for a in div.find_all("a", href=True):
                        link = a['href']
                        if self.key in link:
                            if link not in cars_links:
                                cars_links.append(link)

            else:
                continue

        self.links_to_download = cars_links

    def parser_image_page(self):
        save_number_to_array = []

        for link in self.links_to_download:
            print(f"Parsing image page number {link} is started ...")

            if 'http' not in link:
                url = self.url + link[1:]
            else:
                link = str(link).split('/')
                link = '/' + link[3] + '/' + link[4]
                url = self.url + link[1:]

            html = self._request(url)
            soup = BeautifulSoup(html, 'html.parser')

            if soup is not None:
                number = soup.find("h1", {"class": "pull-left"}).contents[0].strip()
                save_number_to_array.append([link, number])
            else:
                continue

        self.csv = save_number_to_array

    def get_images(self):
        if len(self.csv) > 0:
            images_array = np.array(self.csv)[:, :1]
        else:
            print("Check your URL")
            exit()

        folder = images_array[0][0].split('/')[1]

        if not os.path.exists('./' + folder):
            os.mkdir('./' + folder)

        chrome = Chrome()

        for link in images_array:

            image_name = '.' + link[0] + '.jpg'
            image_url = link[0].replace('nomer', 'foto')[1:]
            url = self.url + image_url
            html = self._request(url)
            soup = BeautifulSoup(html, 'html.parser')

            if soup is not None:

                image_src = soup.find("img", {"class": "img-responsive center-block"})
                link = image_src['src']
                code = requests.get(link).status_code

                if code == 200 or code == 403:
                    print(link, "download image to", image_name)
                    chrome.download_image(link, image_name)
                else:
                    print("There is no link", link, "The error is:", code)

            else:
                continue

        chrome.logout()

    def create_csv(self):
        df = pd.DataFrame(self.csv, columns=["image_path", "code"])
        df.image_path = df.image_path + ".jpg"
        csv_name_country = df.image_path[0].split("/")[1]
        csv_name_time = str(datetime.date(datetime.now())).replace("-", "_")
        csv_name = csv_name_country + "_" + csv_name_time + "_" + str(np.random.randint(1000, size=1)[0]) + ".csv"
        df.to_csv(csv_name)

