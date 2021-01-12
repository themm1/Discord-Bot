import discord
from discord.ext import commands
from functions import element, edit_string
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from functions import get_numbers, edit_string, element


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

class MovieRating:
    def __init__(self, platform, rating, rater):
        self.platform = platform
        self.rating = rating
        self.rater = rater

def get_movie_info(driver):
    imdb_shortcut_1 = "//*[@id='title-overview-widget']/div[1]/div[2]/div/div[2]/div[2]/"
    imdb_shortcut_2 = "//*[@id='title-overview-widget']/div[2]/div[1]/"
    element(driver, By.XPATH, "(//div[@id='web']/descendant::li[@class='first'])[1]/descendant::a[1]").click()
    driver.close()
    driver.switch_to_window(driver.window_handles[0])
    title = driver.find_element_by_xpath(f"{imdb_shortcut_1}h1")
    time = driver.find_element_by_xpath(f"{imdb_shortcut_1}div/time")
    genre = driver.find_element_by_xpath(f"{imdb_shortcut_1}div/a[1]")
    try:
        summary = driver.find_element_by_xpath(f"{imdb_shortcut_2}div[1]/div/div[1]")
    except:
        summary = driver.find_element_by_class_name("summary_text")
    try:
        director = driver.find_element_by_xpath(f"{imdb_shortcut_2}div[2]")
    except:
        director = driver.find_element_by_xpath("//*[@id='title-overview-widget']/div[2]/div[2]/div[1]/div[2]")
    try:
        cast = driver.find_element_by_xpath(f"{imdb_shortcut_2}div[4]")
    except:
        cast = driver.find_element_by_xpath("//*[@id='title-overview-widget']/div[2]/div[2]/div[1]/div[4]")
    try:
        img = driver.find_element_by_xpath("//*[@id='title-overview-widget']/div[1]/div[3]/div[1]/a/img")
    except:
        img = driver.find_element_by_xpath("//*[@id='title-overview-widget']/div[2]/div[1]/a/img")
    summary = edit_string(summary.text, "\nEN", "")
    director = director.text
    cast = edit_string(cast.text, " | See full cast & crew »", "")
    img = img.get_attribute("src")
    return Movie(title.text, time.text, genre.text, summary, director, cast, driver.current_url, img)

def movie_embed(movie, imdb, rt, metacritic):
    stream = movie.stream_movie()
    embed = discord.Embed(title=movie.title, description=f"{movie.summary}\n\nMore information: [IMDb]({movie.url})\
        \nWatch for free: [AZMovies]({stream}) (NOT SECURE)", color=0xFF0000)
    embed.set_thumbnail(url=movie.img)
    embed.add_field(name="Genre", value=movie.genre, inline=True)
    embed.add_field(name="Runtime", value=movie.time, inline=True)
    embed.add_field(name="Credits", value=f"{movie.director}\n{movie.cast}", inline=False)
    for site in imdb, rt, metacritic:
        if site.rating.isnumeric():
            movie_rating = f"{site.rating} % ({site.rater} rating)"
        else:
            movie_rating = site.rating
        embed.add_field(name=site.platform, value=f"{movie_rating}", inline=True)
    return embed

def main_movie(movie):
    try:
        rt_rating = movie.number(By.CLASS_NAME, "rottenTomatoes")
    except:
        rt_rating = "None"
    driver = movie.driver
    movie_info = get_movie_info(driver)
    imdb_rating = movie.number(By.XPATH, "//*[@id='title-overview-widget']/div[1]/div[2]/div/div[1]/div[1]/div[1]/strong/span")
    mc_rating = movie.number(By.XPATH, "//*[@id='title-overview-widget']/div[2]/div[3]/div[1]/a/div")
    imdb = MovieRating("IMDb", imdb_rating, "Audience")
    rotten_tomatoes = MovieRating("Rotten Tomatoes", rt_rating, "Critic")
    metacritic = MovieRating("Metacritic", mc_rating, "Critic")
    embed = movie_embed(movie_info, imdb, rotten_tomatoes, metacritic)
    return embed