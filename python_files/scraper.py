from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from functions import element, get_numbers

class Scraper: 
    def __init__(self, driver, user_input, site):
        self.driver = driver
        self.user_input = user_input
        driver.get(site)

    def number(self, by_x, html_element):
        try:
            data = element(self.driver, by_x, html_element)
            return get_numbers(data.text)
        except:
            return "Unavailable"

    def click_element(self, by_x, html_element):
        element(self.driver, by_x, html_element).click()

    def get_element(self, html_element):
        return self.driver.find_element_by_xpath(html_element).text

    def get_current_url(self):
        return self.driver.current_url

    def close(self):
        self.driver.close()

    def quit(self):
        self.driver.quit()