import discord
from discord.ext import commands

def wot_embed(player):
    p = player
    embed = discord.Embed(title=f"{p.name} ({p.clan})", description=f"More stats: \
    [WotCharts]({p.wotcharts}), [WotLife]({p.wotlife})", color=0xFF0000)
    embed.add_field(name="Battles", value=p.battles[0], inline=True)
    embed.add_field(name="Winrate", value=p.winrate[0], inline=True)
    embed.add_field(name="WN8", value=p.wn8[0], inline=True)
    i = 0
    for session in "Last 24 hours", "Last 7 days", "Last 30 days":
        i += 1
        embed.add_field(name=session, value=f"{p.battles[i]}\n{p.winrate[i]}\n{p.wn8[i]}", inline=True)
    return embed

def movie_embed(movie, imdb, rt, metacritic):
    stream = movie.stream_movie()
    embed = discord.Embed(title=movie.title, description=f"{movie.summary}\n\nMore information: [IMDb]({movie.url})\
        \nWhatch for free: [AZMovies]({stream}) (NOT SECURE)", color=0xFF0000)
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