import os
import platform
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


operating_system = platform.platform()

if 'Windows' in operating_system:
    DOWNLOAD_DIR = str(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + "\\pics\\010_new\\"
else:
    DOWNLOAD_DIR = str(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + "/pics/010_new"


chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument('--start-maximized')
if 'Windows' not in operating_system:
    chrome_options.add_argument("--headless")

prefs = {"download.default_directory": DOWNLOAD_DIR}
chrome_options.add_experimental_option("prefs", prefs)


class Browser:
    browser, service = None, None

    def __init__(self):
        self.browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    def add_input(self, by: By, id: str, value: str):
        field = self.browser.find_element(by=by, value=id)
        field.clear()
        field.send_keys(value)
        time.sleep(1)

    def click_button(self, by: By, id: str):
        button = self.browser.find_element(by=by, value=id)
        button.click()
        time.sleep(1)

    def click_if_not_selected(self, by: By, id: str):
        button = self.browser.find_element(by=by, value=id)
        ancestors = button.find_elements(By.XPATH, ".//ancestor::*")
        parent_div = ancestors[-2]

        selected = 'selected' in parent_div.get_attribute('class')
        if not selected:
            button.click()

        time.sleep(1)

    def close(self):
        self.browser.close()

    def find_element(self, by: By, id: str):
        el = self.browser.find_element(by=by, value=id)
        return el

    def open_page(self, url: str):
        self.browser.get(url)

    def sleep(self, timeout: int):
        time.sleep(timeout)

    def wait_and_click(self, by: By, id: str, timeout: int):
        wait = WebDriverWait(self.browser, timeout)
        wait.until(EC.presence_of_element_located((by, id)))
        self.browser.find_element(by=by, value=id).click()
