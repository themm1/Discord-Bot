import os
import random
import discord
from discord.ext import commands
from sys import platform
from movie_scraper import Scraper
from scrape_func import chrome_setup, chrome_setup_win
from functions import movie_embed, process_ratings

# check OS
if platform == "win32":
    HEROKU = False
    from bot_token import TOKEN
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

@client.event
async def on_member_join(member):
    print(f"{member} has joined a server")

@client.event
async def on_memver_remove(member):
    print(f"{member} has left a server")
 
@client.command()
async def ping(ctx):
    latency = round(client.latency * 1000)
    await ctx.send(f"Pong! {latency} ms")

@client.command(aliases=["8ball"])
async def _8ball(ctx, *, question):
    responses = ["It is certain",
                 "Without a doubt",
                  "Sure",
                  "Yes.",
                  "Ask again later",
                  "No.",
                  "Very doubtful"]
    random_answer = random.choice(responses)
    await ctx.send(f"Question: {question}\nAnswer: {random_answer}")

@client.command(aliases=["movie", "film"])
async def movieScraper(ctx, *, film):
    try:
        movie = Scraper(driver, film)
        movie_embed = process_ratings(movie)
        await ctx.send(embed=movie_embed)
    except:
        await ctx.send("Sorry, we couldn't find the movie")

if HEROKU:
    client.run(os.environ["BOT_TOKEN"])
else:
    client.run(TOKEN)