import os
import random
import discord
from discord.ext import commands
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


try:
    from secret import TOKEN, API_KEY
except:
    TOKEN = os.environ["BOT_TOKEN"]
    API_KEY = os.environ["API_KEY"]

client.run(TOKEN)