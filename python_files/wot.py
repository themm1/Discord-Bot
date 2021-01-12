import discord
from discord.ext import commands
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

class WotPlayer:
    def __init__(self, name, clan, battles, winrate, wn8):
        self.name = name
        self.clan = clan
        self.battles = battles
        self.winrate = winrate
        self.wn8 = wn8
        self.wotlife = f"https://sk.wot-life.com/eu/player/{self.name}/"
        self.wotcharts = f"https://wotcharts.eu/Player?name={self.name}"

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