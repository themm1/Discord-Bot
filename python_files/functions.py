import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def chrome_linux(options):
    options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    options.add_argument("--headless")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=options)
    return driver

def chrome_win(options):
    # options.add_argument("headless")
    driver = webdriver.Chrome(executable_path="C:\Programming Modules\Drivers\chromedriver.exe", options=options)
    return driver

def chrome_setup(HEROKU):
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    if HEROKU:
        driver = chrome_linux(options)
    else:
        driver = chrome_win(options)
    accept_yahoo_cookies(driver)
    return driver

def accept_yahoo_cookies(driver):
    driver.get("https://www.yahoo.com/")
    try:
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.NAME,"agree"))).click()
    except:
        pass

def element(driver, by_x, html_element):
    try:
        element = WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((by_x, html_element))
        )
        return element
    except:
        return False

def get_numbers(string):
    numbers_list = [string[i] for i in range(len(string)) if string[i].isnumeric()]
    number = "".join(numbers_list)
    return number

def edit_string(string, chars, replace):
    try:
        string = string.replace(chars, replace)
    except:
        string = string
    return string