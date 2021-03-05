import os
import random
import discord
from discord.ext import commands
from sys import platform
from movies import imdb_main, movie_embed, series_embed
from wot import getWotStats, wotEmbed


client = commands.Bot(command_prefix="!", help_command=None)


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="!help for commands"))
    print("Bot is ready.")
 
@client.command(aliases=["movie", "film"])
async def movies(ctx, *, film):
    try:
        movie = imdb_main(film, "movie", API_KEY)
        embed = movie_embed(movie)
        await ctx.send(embed=embed)
    except:
        await ctx.send("Couldn't find the movie")

@client.command(aliases=["serial", "series"])
async def serials(ctx, *, series):
    try:
        serial = imdb_main(series, "series", API_KEY)
        embed = series_embed(serial)
        await ctx.send(embed=embed)
    except:
        await ctx.send("Couldn't find the series")
    
@client.command()
async def wot(ctx, *, player_name):
    player = getWotStats(player_name)
    wot_embed = wotEmbed(player)
    await ctx.send(embed=wot_embed)
    
@client.command(aliases=["rn", "randomnumber"])
async def random_number(ctx, max_nubmer):
    try:
        rn = random.randint(1, int(max_nubmer))
        await ctx.send(f"Random number: **{rn}**")
    except:
        await ctx.send("Couldn't generate random number. Example: !rn 10")

@client.command()
async def ping(ctx):
    latency = round(client.latency * 1000)
    await ctx.send(f"Your ping is {latency} ms")

@client.command(aliases=["commands"])
async def help(ctx):
    embed = discord.Embed(title="Commands", description="\
        Code on [GitHub](https://github.com/themm1/Discord-Bot)", color=0x31FF00)
    embed.add_field(name="Command", value="\
        \n__**!ping**__\n\n__**!rn [nubmer]**__\n\n__**!wot [player]**__\n\n\
        __**!movie [movie]**__\n\n__**!series [series]**__", inline=True)
    embed.add_field(name="Message", value="\
        \nyour ping to the discord server\n\ngenerates random number in range 1 - [the number]\n\n\
        WoT player's stats\n\ninforamtion about the movie\n\ninforamtion about the series", inline=True)
    
    await ctx.send(embed=embed)


def chrome_linux(options):
    options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    options.add_argument("--headless")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1420,1080")
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
    from secret import TOKEN, API_KEY
    driver = chrome_setup(HEROKU=False)
else:
    TOKEN = os.environ["BOT_TOKEN"]
    API_KEY = os.environ["API_KEY"]
    driver = chrome_setup(HEROKU=True)

client.run(TOKEN)