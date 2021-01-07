from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from scrape_func import get_numbers, edit_string, element

# movie information class
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

# movie rating class
class MovieRating:
    def __init__(self, platform, rating, rater):
        self.platform = platform
        self.rating = rating
        self.rater = rater

# class for scraping information from Yahoo and IMDb
class Scraper: 
    def __init__(self, driver, film):
        self.driver = driver
        self.film = film
        driver.get(f"https://search.yahoo.com/search?p=imdb+{self.film}")

    # get basic information about movie and create object from Movie class
    def info(self):
        imdb_shortcut_1 = "//*[@id='title-overview-widget']/div[1]/div[2]/div/div[2]/div[2]/"
        imdb_shortcut_2 = "//*[@id='title-overview-widget']/div[2]/div[1]/"
        element(self.driver, By.XPATH, "(//div[@id='web']/descendant::li[@class='first'])[1]/descendant::a[1]").click()
        self.driver.close()
        self.driver.switch_to_window(self.driver.window_handles[0])
        title = self.driver.find_element_by_xpath(f"{imdb_shortcut_1}h1")
        time = self.driver.find_element_by_xpath(f"{imdb_shortcut_1}div/time")
        genre = self.driver.find_element_by_xpath(f"{imdb_shortcut_1}div/a[1]")
        try:
            summary = self.driver.find_element_by_xpath(f"{imdb_shortcut_2}div[1]/div/div[1]")
        except:
            summary = self.driver.find_element_by_class_name("summary_text")
        summary = edit_string(summary.text, "\nEN")
        try:
            director = self.driver.find_element_by_xpath(f"{imdb_shortcut_2}div[2]")
        except:
            director = self.driver.find_element_by_xpath("//*[@id='title-overview-widget']/div[2]/div[2]/div[1]/div[2]")
        director = director.text
        try:
            cast = self.driver.find_element_by_xpath(f"{imdb_shortcut_2}div[4]")
        except:
            cast = self.driver.find_element_by_xpath("//*[@id='title-overview-widget']/div[2]/div[2]/div[1]/div[4]")
        cast = edit_string(cast.text, " | See full cast & crew »")
        try:
            img = self.driver.find_element_by_xpath("//*[@id='title-overview-widget']/div[1]/div[3]/div[1]/a/img")
        except:
            img = self.driver.find_element_by_xpath("//*[@id='title-overview-widget']/div[2]/div[1]/a/img")
        img = img.get_attribute("src")
        return Movie(title.text, time.text, genre.text, summary, director, cast, self.driver.current_url, img)

    # get rating
    def rating(self, by_x, html_element):
        try:
            data = element(self.driver, by_x, html_element)
            return get_numbers(data.text)
        except:
            return "Rating unavailable"

    def get_current_url(self):
        return self.driver.current_url

    def close(self):
        self.driver.close()

    def quit(self):
        self.driver.quit()