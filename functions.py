import discord
from discord.ext import commands
from movie_classes import MovieRating, WotPlayer
from selenium.webdriver.common.by import By

def wot_info(wot):
    battles = {}; winrate = {}; wn8 = {}
    name = wot.get_element("/html/body/div[4]/div/div/div/h3")
    clan = wot.get_element("/html/body/div[4]/div/div/div/p/b/font/a[1]")
    for i in range(1, 5):
        battles[i] = wot.get_element(f"//*[@id='random']/table/tbody/tr[2]/td[{i}]")
        winrate[i] = wot.get_element(f"//*[@id='random']/table/tbody/tr[4]/td[{i}]")
        wn8[i] = wot.get_element(f"//*[@id='random']/table/tbody/tr[9]/td[{i}]")
    wot.close()
    if clan == "[]":
        clan = "Without clan"
    return WotPlayer(name, clan, battles, winrate, wn8)

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