import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# chrome setup (open chrome, accept cookies)
def chrome_setup():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
    driver.get("https://www.yahoo.com/")
    try:
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.NAME,"agree"))).click()
    except:
        pass
    return driver

# function for WebDriverWait
def element(driver, by_x, html_element):
    try:
        element = WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((by_x, html_element))
        )
        return element
    except:
        print("Couldn't find the element")
        return "Element not found"

# get numbers from string
def get_numbers(string):
    numbers_list = [string[i] for i in range(len(string)) if string[i].isnumeric()]
    number = "".join(numbers_list)
    return number

# remove certain charasters from a string
def edit_string(string, chars):
    try:
        string = string.replace(chars, "")
    except:
        string = string
    return string