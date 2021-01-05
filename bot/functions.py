import discord
from discord.ext import commands
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from scraper import Movie, MovieRating

# chrome setup (open chrome, accept cookies)
def chrome_setup():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_argument("headless")
    driver = webdriver.Chrome(executable_path="C:\Programming Modules\Drivers\chromedriver.exe", options=options)
    driver.get("https://www.google.com/")
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME,"agree"))).click()
    except:
        pass
    return driver

def movie_embed(movie, imdb, rt, metacritic):
    embed = discord.Embed(title=movie.title, description=f"{movie.summary}\n\nMore information [here]({movie.url})", color=0xFF0000)
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

def process_ratings(movie):
    try:
        rt_rating = movie.rating(By.CLASS_NAME, "rottenTomatoes")
    except:
        rt_rating = "None"
    movie_info = movie.info()
    imdb_rating = movie.rating(By.XPATH, "//*[@id='title-overview-widget']/div[1]/div[2]/div/div[1]/div[1]/div[1]/strong/span")
    mc_rating = movie.rating(By.XPATH, "//*[@id='title-overview-widget']/div[2]/div[3]/div[1]/a/div")
    imdb = MovieRating("IMDb", imdb_rating, "Audience")
    rotten_tomatoes = MovieRating("Rotten Tomatoes", rt_rating, "Critic")
    metacritic = MovieRating("Metacritic", mc_rating, "Critic")
    embed = movie_embed(movie_info, imdb, rotten_tomatoes, metacritic)
    return embed