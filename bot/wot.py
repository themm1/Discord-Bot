import discord
from discord.ext import commands
from requests_html import HTMLSession


def getWotStats(player):
    session = HTMLSession()
    site = session.get(f"https://sk.wot-life.com/eu/player/{player}")

    name = site.html.find("#title > div > div > h1")[0].text
    try:
        clan = site.html.find(".col-xs-12.col-sm-dyn.col-sm-pull-right > .clan > .clan-info > .clan-tag > a")[0].text
    except Exception:
        clan = ""

    battles = []; winrate = []; wn8 = [];
    for i in range(4):
        battles.append(site.html.find(f"tbody > tr:nth-child(1) > td.text-right")[i].text)
        winrate.append(site.html.find(f"tbody > tr:nth-child(3) > td:nth-child(3)")[i].text)
        wn8.append(site.html.find(f"tbody > tr:nth-child(15) > .text-right.wn")[i].text)
            
    return WotPlayer(name, clan, battles, winrate, wn8)

def wotEmbed(player):
    p = player
    embed = discord.Embed(title=f"{p.name} {p.clan}", description=f"More stats: \
    [WotCharts]({p.wotcharts}), [WotLife]({p.wotlife})", color=0x00F4FF)
    embed.add_field(name="Battles", value=p.battles[0], inline=True)
    embed.add_field(name="Winrate", value=p.winrate[0], inline=True)
    embed.add_field(name="WN8", value=p.wn8[0], inline=True)

    i = 0
    for session in "Last 24 hours", "Last 7 days", "Last 30 days":
        i += 1
        embed.add_field(name=session, value=f"{p.battles[i]}\n{p.winrate[i]}\n{p.wn8[i]}", inline=True)
    return embed


class WotPlayer:
    def __init__(self, name, clan, battles, winrate, wn8):
        self.name = name
        self.clan = clan
        self.battles = battles
        self.winrate = winrate
        self.wn8 = wn8
        self.wotlife = f"https://sk.wot-life.com/eu/player/{name}"
        self.wotcharts = f"https://wotcharts.eu/Player?name={name}"