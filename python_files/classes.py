from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from scraping_functions import get_numbers, edit_string, element

class Movie:
    def __init__(self, title, time, genre, summary, director, cast, url, img):
        self.title = title
        self.time = time
        self.genre = genre
        self.summary = summary
        self.director = director
        self.cast = cast
        self.url = url
        self.img = img

    def stream_movie(self):
        url_title = edit_string(self.title, " ", "-")
        url_title = url_title[:-7].lower()
        return f"https://azm.to/movie/{url_title}"

class WotPlayer:
    def __init__(self, name, clan, battles, winrate, wn8):
        self.name = name
        self.clan = clan
        self.battles = battles
        self.winrate = winrate
        self.wn8 = wn8
        self.wotlife = f"https://sk.wot-life.com/eu/player/{self.name}/"
        self.wotcharts = f"https://wotcharts.eu/Player?name={self.name}"

class MovieRating:
    def __init__(self, platform, rating, rater):
        self.platform = platform
        self.rating = rating
        self.rater = rater

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