import json
import asyncio
import requests
from pprint import pprint

async def stream_notifications(client, API_HEADERS):
    with open("bot/notifications.json") as f:
        ids = json.load(f)

    live = {}
    for id in ids.keys():
        live[id] = False

    while True:
        for streamer_id in ids.keys():
            stream = check_stream(streamer_id, API_HEADERS)
                
            if stream != False and live[streamer_id] == False:
                live[streamer_id] = True
                message = f"{stream['user_name']} is streaming {stream['game_name']}\n"\
                f"{stream['title']}, {stream['url']}"

                for channel_id in ids[streamer_id]:
                    channel = client.get_channel(channel_id)
                    await channel.send(message)

            elif stream == False and live[streamer_id] == True:
                live[streamer_id] = False
            await asyncio.sleep(10)

def get_user_id(username, API_HEADERS):
    url = f"https://api.twitch.tv/helix/users?login={username}"
    user = requests.get(url, headers=API_HEADERS).json()
    pprint(user)


def get_headers(twitch_keys):
    body = {
        "client_id": twitch_keys['client_id'],
        "client_secret": twitch_keys['client_secret'],
        "grant_type": "client_credentials"
    }
    r = requests.post("https://id.twitch.tv/oauth2/token", body)
    keys = r.json();

    API_HEADERS = {
        "Client-ID": twitch_keys['client_id'],
        "Authorization": f"Bearer {keys['access_token']}"
    }
    return API_HEADERS

def check_stream(user_id, API_HEADERS):
    url = f"https://api.twitch.tv/helix/streams?user_id={user_id}"
    stream = False

    try:
        stream_info = requests.get(url, headers=API_HEADERS).json()
        if stream_info['data']:
            stream = stream_info['data'][0]
            url = f"https://www.twitch.tv/{stream['user_login']}"
            stream['url'] = url
    except Exception as e:
        print(f"Error checking user: {e}")
    return stream