from embeds import wot_embed, movie_embed
from functions import element, edit_string
from classes import MovieRating, WotPlayer, Movie
from selenium.webdriver.common.by import By

def main_wot_stats(wot):
    try:
        wot.click_element(By.XPATH, "//*[@id='consentDialog']/div[2]/div[2]/div/div[2]/div/div[1]/div")
        clan = wot.get_element("//*[@id='title']/div/div[2]/div/div/div[1]")
    except:
        clan = "Without clan"
    battles = []; winrate = []; wn8 = []
    name = wot.get_element("//*[@id='title']/div/div/h1")
    for i in range(2, 9, 2):
        winrate.append(wot.get_element(f"//*[@id='tab1']/table[1]/tbody/tr[4]/td[{i}]"))
    for i in range(1, 5):
        battles.append(wot.get_element(f"//*[@id='tab1']/table[1]/tbody/tr[2]/td[{i}]"))
        wn8.append(wot.get_element(f"//*[@id='tab1']/table[1]/tbody/tr[16]/td[{i}]"))
    player = WotPlayer(name, clan, battles, winrate, wn8)
    embed = wot_embed(player)
    return embed

def main_movie(movie):
    try:
        rt_rating = movie.number(By.CLASS_NAME, "rottenTomatoes")
    except:
        rt_rating = "None"
    driver = movie.driver
    movie_info = get_movie_info(driver)
    imdb_rating = movie.number(By.XPATH, "//*[@id='title-overview-widget']/div[1]/div[2]/div/div[1]/div[1]/div[1]/strong/span")
    mc_rating = movie.number(By.XPATH, "//*[@id='title-overview-widget']/div[2]/div[3]/div[1]/a/div")
    imdb = MovieRating("IMDb", imdb_rating, "Audience")
    rotten_tomatoes = MovieRating("Rotten Tomatoes", rt_rating, "Critic")
    metacritic = MovieRating("Metacritic", mc_rating, "Critic")
    embed = movie_embed(movie_info, imdb, rotten_tomatoes, metacritic)
    return embed

def get_movie_info(driver):
    imdb_shortcut_1 = "//*[@id='title-overview-widget']/div[1]/div[2]/div/div[2]/div[2]/"
    imdb_shortcut_2 = "//*[@id='title-overview-widget']/div[2]/div[1]/"
    element(driver, By.XPATH, "(//div[@id='web']/descendant::li[@class='first'])[1]/descendant::a[1]").click()
    driver.close()
    driver.switch_to_window(driver.window_handles[0])
    title = driver.find_element_by_xpath(f"{imdb_shortcut_1}h1")
    time = driver.find_element_by_xpath(f"{imdb_shortcut_1}div/time")
    genre = driver.find_element_by_xpath(f"{imdb_shortcut_1}div/a[1]")
    try:
        summary = driver.find_element_by_xpath(f"{imdb_shortcut_2}div[1]/div/div[1]")
    except:
        summary = driver.find_element_by_class_name("summary_text")
    try:
        director = driver.find_element_by_xpath(f"{imdb_shortcut_2}div[2]")
    except:
        director = driver.find_element_by_xpath("//*[@id='title-overview-widget']/div[2]/div[2]/div[1]/div[2]")
    try:
        cast = driver.find_element_by_xpath(f"{imdb_shortcut_2}div[4]")
    except:
        cast = driver.find_element_by_xpath("//*[@id='title-overview-widget']/div[2]/div[2]/div[1]/div[4]")
    try:
        img = driver.find_element_by_xpath("//*[@id='title-overview-widget']/div[1]/div[3]/div[1]/a/img")
    except:
        img = driver.find_element_by_xpath("//*[@id='title-overview-widget']/div[2]/div[1]/a/img")
    summary = edit_string(summary.text, "\nEN", "")
    director = director.text
    cast = edit_string(cast.text, " | See full cast & crew »", "")
    img = img.get_attribute("src")
    return Movie(title.text, time.text, genre.text, summary, director, cast, driver.current_url, img)