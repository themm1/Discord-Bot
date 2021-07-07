import discord
import requests
from pprint import pprint

class FaceitStats:
    def __init__(self, player_name, api_token):
        self.player_name = player_name
        self.base_url = "https://open.faceit.com/data/v4"

        self.headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {api_token}"
        }
        self.player = self.get_player()
        self.player.update(self.get_stats()['lifetime'])

    def get_player(self):
        results = requests.get(f"{self.base_url}/search/players", headers=self.headers, params={"nickname": self.player_name}).json()
        player_id = results['items'][0]['player_id']
        player = requests.get(f"{self.base_url}/players/{player_id}", headers=self.headers).json()

        if player['avatar'] == "":
            player.pop("avatar")
            player['avatar'] = "https://pbs.twimg.com/profile_images/1349712390628270081/KpMEtOII.png"

        player['elo'] = player['games']['csgo']['faceit_elo']
        player['level'] = player['games']['csgo']['skill_level']
        return player

    def get_stats(self):
        stats = requests.get(f"{self.base_url}/players/{self.player['player_id']}/stats/csgo", headers=self.headers)
        return stats.json()

def faceit_embed(player):
    embed = discord.Embed(title=player['nickname'], description=f"""
    Steam: [**{player['steam_nickname']}**](https://steamcommunity.com/profiles/{player['steam_id_64']})
    Faceit: [**{player['nickname']}**](https://www.faceit.com/en/players/{player['nickname']})""", color=0xFF5E00)
    embed.set_thumbnail(url=player['avatar'])

    embed.add_field(name="ELO", value=f"{player['games']['csgo']['faceit_elo']} "\
    f"(level {player['games']['csgo']['skill_level']})", inline=True)
    embed.add_field(name="K/D", value=player['Average K/D Ratio'], inline=True)
    embed.add_field(name="Winrate", value=f"{player['Win Rate %']}%", inline=True)

    for i in range(len(player['Recent Results'])):
        if player['Recent Results'][i] == "0":
            player['Recent Results'][i] = "L"
        else:
            player['Recent Results'][i] = "W"

    embed.add_field(name="Matches", value=player['Matches'], inline=True)
    embed.add_field(name="Recent Results", value=" ".join(player['Recent Results']), inline=True)
    embed.add_field(name="Longest Win Streak", value=player['Longest Win Streak'], inline=True)

    return embed
