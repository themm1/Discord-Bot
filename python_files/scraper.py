from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Scraper: 
    def __init__(self, driver, user_input, site):
        self.driver = driver
        self.user_input = user_input
        driver.get(site)

    def click_element(self, by_x, html_element):
        try:
            element = self.driver(self.driver, 1).until(
                EC.presence_of_element_located((by_x, html_element))
            )
        except:
            return False

    def get_element(self, html_element):
        return self.driver.find_element_by_xpath(html_element).text

    def get_current_url(self):
        return self.driver.current_url

    def close(self):
        self.driver.close()

    def quit(self):
        self.driver.quit()