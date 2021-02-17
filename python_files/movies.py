import discord
from discord.ext import commands
from imdb import IMDb
from rotten_tomatoes_client import RottenTomatoesClient

class movieInfo:
    def __init__(self, title, year, plot, genres, runtime, directors, cast):
        self.title = title
        self.year = year
        self.plot = plot
        self.genres = genres
        self.runtime = runtime
        self.directors = directors
        self.cast = cast

    def general(self):
        self.title = f"{self.title} ({self.year})"

        plot = self.plot[0]
        self.plot = plot.split("::", 1)[0]

        self.genres = ", ".join(self.genres)

        runtime = int(self.runtime[0])
        runtime = runtime / 60
        mins = runtime % 10 / 10 * 60
        self.runtime = f"{int(runtime)}h {int(mins)}min"

    def credits(self):
        directors = []
        for director in self.directors:
            directors.append(director['name'])
        self.directors = ", ".join(directors)

        cast = []
        for i in range(3):
            cast.append(self.cast[i]['name'])
        self.cast = ", ".join(cast) 


class movieRatings:
    def __init__(self, imdb, rottentom, metacritic):
        self.imdb = imdb
        self.rottentom = rottentom
        self.metacritic = metacritic
        

    def format(self):
        self.imdb['rating'] = int(self.imdb['rating']*10)
        self.imdb['url'] = f"https://www.imdb.com/title/tt{self.imdb['id']}"

        self.rottentom['rating'] = self.rottentom['meterScore']
        self.rottentom['url'] = f"https://www.rottentomatoes.com{self.rottentom['url']}"
        
        self.metacritic['rating'] = self.metacritic['metascore']
        self.metacritic['url'] = self.metacritic['metacritic url']


def imdbInfo(query):
    ia = IMDb()
    search = ia.search_movie(query)
    movie_id = search[0].getID()
    movie = ia.get_movie(movie_id)
    metacritic = ia.get_movie_critic_reviews(movie_id)["data"]
    movie["metacritic"] = metacritic
    movie["id"] = movie_id
    return movie
    
def movieSearch(title):
    result = RottenTomatoesClient.search(term=title, limit=5)
    return result["movies"][0]


def movie_main(film):
    movie = imdbInfo(film)

    info = movieInfo(movie['title'], movie['year'], movie['plot'], movie['genres'],
                        movie['runtime'], movie['directors'], movie['cast'])
    info.general()
    info.credits()

    imdb = {"platform": "IMDb", "rating": movie['rating'], "id": movie['id']}
    rottentom = movieSearch(movie['title'])
    rottentom['platform'] = "Rotten Tomatoes"
    metacritic = movie['metacritic']
    metacritic['platform'] = "Metacritic"

    ratings = movieRatings(imdb, rottentom, metacritic)
    ratings.format()
    return {"info": info, "ratings": ratings}

def movie_embed(movie):
    info = movie['info']
    ratings = movie['ratings']
    
    embed = discord.Embed(title=info.title, description=f"{info.plot}\n\nMore information: [IMDb]({ratings.imdb['url']})\
        \nWatch for free: AZMovies (NOT SECURE)", color=0xFF0000)
        
    embed.set_thumbnail(url="url")
    embed.add_field(name="Genre", value=info.genre, inline=True)
    embed.add_field(name="Runtime", value=info.runtime, inline=True)
    embed.add_field(name="Credits", value=f"{info.directors}\n{info.cast}", inline=False)

    for site in ratings.imdb, ratings.rottentom, ratings.metacritic:
        embed.add_field(name=site['platform'], value=site['rating'], inline=True)
    return embed