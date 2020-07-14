from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import platform


class Chrome(Options):

    def __init__(self):
        super(Chrome, self).__init__()
        self.options = Options()
        self.options.add_argument("--headless")
        self.options.add_argument("window-size=1920,1080")

        type_of_os = platform.system()
        print(type_of_os)
        if type_of_os == "Windows":
            self.driver = webdriver.Chrome(executable_path='./win/chromedriver.exe', chrome_options=self.options)
        elif type_of_os == "Linux":
            self.options.add_argument('--headless')
            self.options.add_argument('--disable-infobars')
            self.options.add_argument('--disable-dev-shm-usage')
            self.options.add_argument("--no-sandbox")
            self.options.add_argument("--remote-debugging-port=9222")
            self.driver = webdriver.Chrome(executable_path='./linux/chromedriver', chrome_options=self.options)
        elif type_of_os == "Mac":
            self.driver = webdriver.Chrome(executable_path='./mac/chromedriver', chrome_options=self.options)
        else:
            print("Can not find type of your OS ...")
            exit()

    def download_image(self, url, name):
        """
        :param url: str
        :param name: str
        :return: *jpg
        """
        try:
            driver_url = self.driver.get(url)
            get_image_by_url = self.driver.find_elements_by_name('img')
            image = self.driver.save_screenshot(name)
        except:
            print("Check your internet connect or selenium chrome")

    def logout(self):
        """
        :return: -
        """
        return self.driver.quit()



# chrome = Chrome()
# img = chrome.download_image("http://img03.platesmania.com/200708/o/14991411.jpg", "test.jpg")
# chrome.logout()