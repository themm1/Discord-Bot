import os
import random
import discord
from discord.ext import commands
from selenium import webdriver
from sys import platform
from movies import movie_main, movie_embed
from wot import main_wot_stats
from scraper import Scraper

client = commands.Bot(command_prefix="!")

@client.event
async def on_ready():
    print("Bot is ready.")
 
@client.command(aliases=["movie", "film"])
async def movieScraper(ctx, *, film):
    movie = movie_main(film)
    embed = movie_embed(movie)
    await ctx.send(embed=embed)

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
    return driver


if platform == "win32":
    from token_discord import TOKEN
    driver = chrome_setup(HEROKU=False)
    client.run(TOKEN)
else:
    driver = chrome_setup(HEROKU=True)
    client.run(os.environ["BOT_TOKEN"])