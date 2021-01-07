import os
import random
import discord
from discord.ext import commands
from sys import platform
from movie_classes import Scraper
from scraping_functions import chrome_setup, chrome_setup_win
from functions import movie_embed, process_ratings, wot_info

# check OS
if platform == "win32":
    HEROKU = False
    from token_discord import TOKEN
else:
    HEROKU = True

client = commands.Bot(command_prefix="!")

if HEROKU:
    driver = chrome_setup()
else:
    driver = chrome_setup_win()


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
    player = wot_info(wot)
    for stat in player.name, player.clan, player.battles, player.winrate, player.wn8, player.wotlife, player.labvole:
        await ctx.send(stat)

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

if HEROKU:
    client.run(os.environ["BOT_TOKEN"])
else:
    client.run(TOKEN)