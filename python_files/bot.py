import os
import random
import discord
from discord.ext import commands
from sys import platform
from selenium.webdriver.common.by import By
from classes import Scraper
from functions import chrome_setup, chrome_setup_win
from main_functions import main_movie, main_wot_stats

client = commands.Bot(command_prefix="!")

@client.event
async def on_ready():
    print("Bot is ready.")
 
@client.command(aliases=["movie", "film"])
async def movieScraper(ctx, *, film):
    try:
        movie = Scraper(driver, film, f"https://search.yahoo.com/search?p=imdb+{film}")
        movie_embed = main_movie(movie)
        await ctx.send(embed=movie_embed)
    except:
        await ctx.send("Sorry, we couldn't find the movie")

@client.command()
async def wot(ctx, *, player):
    try:
        wot = Scraper(driver, player, f"https://sk.wot-life.com/eu/player/{player}/")
        wot_embed = main_wot_stats(wot)
        await ctx.send(embed=wot_embed)
    except:
        await ctx.send("Couldn't find the player")
    
@client.command(aliases=["rn", "randomnumber"])
async def random_number(ctx, max_nubmer):
    try:
        rn = random.randint(1, int(max_nubmer))
        await ctx.send("Random number: {}" .format(rn))
    except:
        await ctx.send("Couldn't generate random number. Example: !rn 10")

@client.command()
async def ping(ctx):
    latency = round(client.latency * 1000)
    await ctx.send(f"Your ping is {latency} ms")

# check OS
if platform == "win32":
    from token_discord import TOKEN
    driver = chrome_setup_win()
    client.run(TOKEN)
    HEROKU = False
else:
    driver = chrome_setup()
    client.run(os.environ["BOT_TOKEN"])
    HEROKU = True