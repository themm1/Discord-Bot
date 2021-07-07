import os
import random
import discord
from discord.ext import commands
from wot import getWotStats, wotEmbed
from faceit import faceit_embed, FaceitStats
from movies import imdb_main, movie_embed, series_embed


client = commands.Bot(command_prefix="!", help_command=None)


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="!help for commands"))
    print("Bot is ready.")

@client.command(aliases=["movie", "film"])
async def movies(ctx, *, film):
    try:
        movie = imdb_main(film, "movie", KEYS['omdb'])
        embed = movie_embed(movie)
        await ctx.send(embed=embed)
    except Exception:
        await ctx.send("Couldn't find the movie")

@client.command(aliases=["serial", "series"])
async def serials(ctx, *, series):
    try:
        serial = imdb_main(series, "series", KEYS['omdb'])
        embed = series_embed(serial)
        await ctx.send(embed=embed)
    except Exception:
        await ctx.send("Couldn't find the series")

@client.command(aliases=["faceit", "facieitcs"])
async def faceit_csgo(ctx, name):
    try:
        faceit = FaceitStats(name, KEYS['faceit'])
        embed = faceit_embed(faceit.player)
        await ctx.send(embed=embed)
    except Exception:
        await ctx.send("Couldn't find the player")

@client.command()
async def wot(ctx, *, player_name):
    try:
        player = getWotStats(player_name)
        embed = wotEmbed(player)
        await ctx.send(embed=embed)
    except Exception:
        await ctx.send("Couldn't find the player")

@client.command(aliases=["rn", "randomnumber"])
async def random_number(ctx, max_nubmer):
    try:
        rn = random.randint(1, int(max_nubmer))
        await ctx.send(f"Random number: **{rn}**")
    except Exception:
        await ctx.send("Couldn't generate random number.\n"\
            "Example: **!rn 10**")

@client.command()
async def ping(ctx):
    latency = round(client.latency * 1000)
    await ctx.send(f"Your ping is {latency} ms")

@client.command(aliases=["commands"])
async def help(ctx):
    embed = discord.Embed(title="Commands", description="\
        Code on [GitHub](https://github.com/themm1/Discord-Bot)", color=0x31ff00)
    embed.add_field(name="Command", value="""\n
        **!ping**\n
        **!rn [nubmer]**\n
        **!calc [math expression]**\n
        **!rgb [color code]**\n\n
        **!wot [player]**\n
        **!faceit [player]**\n
        **!movie [movie]**\n
        **!series [series]**""", inline=True)
    embed.add_field(name="Message", value="""\n
        your ping to the discord server\n
        generates random number in range 1 - [the number]\n
        result of the expression (do NOT use spaces)\n
        hexadecimal color if rgb [255,255,255], rgb if hexadecimal [0xffffff]\n
        WoT player's stats\n
        player's Faceit stats (only CS:GO)\n
        inforamtion about the movie\n
        inforamtion about the series""", inline=True)

    await ctx.send(embed=embed)

@client.command(aliases=["math", "result"])
async def calc(ctx, expression):
    result = eval(expression)
    await ctx.send(f"= {result}")

@client.command()
async def rgb(ctx, string):
    ERROR_MESSAGE = "Invalid color code, please try another.\n"\
        "Example: **!rgb 255,255,255** or **!rgb 0xffffff**"
    def hexa(rgb_string):
        rgb_color = rgb_string.split(",")
        hex_color = ["00", "00", "00"]
        for i in range(len(rgb_color)):
            hex_value = hex(int(rgb_color[i]))[2:]
            if len(hex_value) == 1:
                hex_value = f"0{hex_value}"
            elif int(hex_value, 16) > 255:
                hex_value = "ff"
            hex_color[i] = hex_value
        hex_color = "".join(hex_color)
        return f"0x{hex_color}"

    def rgb(hex_string):
        hex_list = [char for char in hex_string]
        if hex_list[0] == "0" and hex_list[1] == "x":
            del hex_list[:2]
        elif hex_list[0] == "#":
            hex_list.pop(0)
        hex_color = [f"{hex_list[i]}{hex_list[i+1]}" for i in range(0, len(hex_list), 2)]
        rgb_color =  [str(int(code, 16)) for code in hex_color]
        if len(rgb_color) == 3:
            return ",".join(rgb_color)
        return ERROR_MESSAGE

    if string[0] == "#" or string[:2] == "0x":
        try:
            await ctx.send(rgb(string))
        except Exception:
            await ctx.send(ERROR_MESSAGE)
    else:
        try:
            await ctx.send(hexa(string))
        except Exception:
            await ctx.send(ERROR_MESSAGE)


try:
    from secret import KEYS
except Exception:
    KEYS = {
        "discord": os.environ['BOT_KEY'],
        "omdb": os.environ['OMDB_KEY'],
        "faceit": os.environ['FACEIT_KEY']
    }

client.run(KEYS['discord'])
