import requests
import discord
from discord.ext import commands


def imdb_main(title, q_type, apiKey):
    data_URL = f"http://www.omdbapi.com/?apikey={apiKey}"

    s_search = {"s": title,    "type": q_type}
    results = requests.get(data_URL, params=s_search).json()

    resultID = results['Search'][0]['imdbID']
    t_search = {"i": resultID,      "type": q_type,    "plot": "full"}
    
    return requests.get(data_URL, params=t_search).json()


def movie_embed(movie):
    stream = f"https://azm.to/movie/{edit_stream(movie['Title'])}"
    
    embed = discord.Embed(title=f"{movie['Title']} ({movie['Year']})", description=f"{movie['Plot']}\
        \n\nMore information on [IMDb](https://www.imdb.com/title/{movie['imdbID']})\
        \nWhatch for free on [AZMovies]({stream}) (NOT SECURE)", color=0xFF0000)
    embed.set_thumbnail(url=movie['Poster'])

    embed.add_field(name="Credits", value=f"Director: {movie['Director']}\nCast: {movie['Actors']}", inline=False)
    embed.add_field(name="Genre", value=movie['Genre'], inline=True)
    embed.add_field(name="Runtime", value=edit_runtime(movie['Runtime']), inline=True)
    embed.add_field(name="Box Office", value=movie['BoxOffice'], inline=True)

    movie['Ratings'][0]['Source'] = "IMDb"
    for site in movie['Ratings']:
        embed.add_field(name=site['Source'], value=f"{edit_number(site['Value'])} %", inline=True)

    return embed


def series_embed(serial):
    embed = discord.Embed(title=f"{serial['Title']} ({serial['Year']})", description=f"{serial['Plot']}\
        \n\nMore information on [IMDb](https://www.imdb.com/title/{serial['imdbID']})", color=0xFF0000)
    embed.set_thumbnail(url=serial['Poster'])

    embed.add_field(name="Credits", value=f"Director: {serial['Director']}\nCast: {serial['Actors']}", inline=False)
    embed.add_field(name="Genre", value=serial['Genre'], inline=True)
    embed.add_field(name="Runtime", value=serial['Runtime'], inline=True)
    embed.add_field(name="IMDb", value=f"{edit_number(serial['Ratings'][0]['Value'])} %", inline=True)

    return embed


def edit_number(ratings):
    value = []
    for rating in ratings:
        if rating == "/":
            break
        elif rating.isnumeric():
            value.append(rating)
    return int("".join(value))

def edit_runtime(runtime):
    runtime = edit_number(runtime)
    runtime = runtime / 60
    mins = runtime % 10 / 10 * 60
    return f"{int(runtime)}h {int(mins)}min"

def edit_stream(title):
    return title.replace(" ", "-").lower()