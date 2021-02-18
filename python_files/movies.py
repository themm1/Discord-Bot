import discord
from discord.ext import commands
from imdb import IMDb
from rotten_tomatoes_client import RottenTomatoesClient

class movieInfo:
    def __init__(self, title, year, plot, genres, runtime, directors, cast, img):
        self.title = title
        self.year = year
        self.plot = plot
        self.genres = genres
        self.runtime = runtime
        self.directors = directors
        self.cast = cast
        self.img = img
        self.stream = self.title.replace(" ", "-").lower()

    def general(self):
        self.title = f"{self.title} ({self.year})"

        plot = self.plot[0]
        self.plot = plot.split("::", 1)[0]

        self.genres = ", ".join(self.genres)

        runtime = int(self.runtime[0])
        runtime = runtime / 60
        mins = runtime % 10 / 10 * 60
        self.runtime = f"{int(runtime)}h {int(mins)}min"

        self.stream = f"https://azm.to/movie/{self.stream}"

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

        try:
            self.rottentom['rating'] = self.rottentom['meterScore']
            self.rottentom['url'] = f"https://www.rottentomatoes.com{self.rottentom['url']}"
        except:
            pass

        try:
            self.metacritic['rating'] = self.metacritic['metascore']
            self.metacritic['url'] = self.metacritic['metacritic url']
        except:
            pass


def imdb_info(query):
    ia = IMDb()
    search = ia.search_movie(query)
    movie_id = search[0].getID()
    movie = ia.get_movie(movie_id)
    metacritic = ia.get_movie_critic_reviews(movie_id)["data"]
    movie["metacritic"] = metacritic
    movie["id"] = movie_id
    return movie
    
def rottentom_search(movie):
    results = RottenTomatoesClient.search(term=movie['title'], limit=10)
    for result in results['movies']:
        if result['year'] == movie['year']:
            return result
    else:
        return {}


def movie_main(film):
    movie = imdb_info(film)

    info = movieInfo(movie['title'], movie['year'], movie['plot'], movie['genres'],
                        movie['runtime'], movie['directors'], movie['cast'], movie['cover url'])
    info.general()
    info.credits()

    imdb = {"platform": "IMDb", "rating": movie['rating'], "id": movie['id']}
    rottentom = rottentom_search(movie)
    rottentom['platform'] = "Rotten Tomatoes"
    metacritic = movie['metacritic']
    metacritic['platform'] = "Metacritic"

    ratings = movieRatings(imdb, rottentom, metacritic)
    ratings.format()
    return {"info": info, "ratings": ratings}

def movie_embed(movie):
    info = movie['info']
    ratings = movie['ratings']
    
    embed = discord.Embed(title=info.title, description=info.plot, color=0xFF0000)
    embed.set_thumbnail(url=info.img)

    embed.add_field(name="Credits", value=f"Directors: {info.directors}\nCast: {info.cast}", inline=False)
    embed.add_field(name="Genre", value=info.genres, inline=True)
    embed.add_field(name="Runtime", value=info.runtime, inline=True)
    embed.add_field(name="Watch for free", value=f"[AZMovies]({info.stream}) (NOT SECURE)")

    for site in ratings.imdb, ratings.rottentom, ratings.metacritic:
        try:
            embed.add_field(name=site['platform'], value=f"[{site['rating']}%]({site['url']})", inline=True)
        except:
            embed.add_field(name=site['platform'], value="Unavailable", inline=True)
    return embed