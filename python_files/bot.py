import os
import random
import discord
from discord.ext import commands
from sys import platform
from selenium.webdriver.common.by import By
from classes import Scraper
from scraping_functions import chrome_setup, chrome_setup_win
from functions import movie_embed, process_ratings, wot_info

# check OS
if platform == "win32":
    from token_discord import TOKEN
    driver = chrome_setup_win()
    HEROKU = False
else:
    driver = chrome_setup()
    HEROKU = True

client = commands.Bot(command_prefix="!")

@client.event
async def on_ready():
    print("Bot is ready.")
 
@client.command(aliases=["movie", "film"])
async def movieScraper(ctx, *, film):
    try:
        movie = Scraper(driver, film, f"https://search.yahoo.com/search?p=imdb+{film}")
        movie_embed = process_ratings(movie)
        await ctx.send(embed=movie_embed)
    except:
        await ctx.send("Sorry, we couldn't find the movie")

@client.command()
async def wot(ctx, *, player):
    wot = Scraper(driver, player, f"https://lab-vole.cz/Player?name={player}")
    wot_embed = wot_info(wot)
    await ctx.send(embed=wot_embed)
        #await ctx.send("Couldn't find the player")
    
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

if platform == "win32":
    client.run(TOKEN)
else:
    client.run(os.environ["BOT_TOKEN"])