from config import STEAM_API_KEY

import requests
import time
import json
import csv
import re

# API endpoints
GET_APP_LIST_URL = f'https://api.steampowered.com/ISteamApps/GetAppList/v0002/?key={STEAM_API_KEY}&format=json' # general list of steam games
APP_DETAILS_URL = f'https://store.steampowered.com/api/appdetails' # detailed list of properties for a specific game ID

response = requests.get(GET_APP_LIST_URL)
games_list_json = response.json()['applist']['apps']

unwanted_game_types_filter= re.compile(r'(demo|deluxe|expansion|soundtrack|ost|dlc|vr|beta|pack|trailer|playtest|bundle|artbook|effect|pose|set|tiles|teaser)', re.IGNORECASE)
explicit_filter = re.compile(r'\b(fuck|sex|porno|xxx|nude|hentai|boobs|fetish|strip|slut|erotic|adult|18+|futanari|femboy|sexy)\b', re.IGNORECASE)
non_western_characters_filter = re.compile(r'[^\x00-\x7F]+')

filtered_games = [
    game for game in games_list_json 
    if game['name'] 
    and not unwanted_game_types_filter.search(game['name'])
    and not explicit_filter.search(game['name'])
    and not non_western_characters_filter.search(game['name'])]

print(len(filtered_games))

#store list of steam game names and ids
with open('final_steam_games.json', 'w') as f:
    json.dump(filtered_games, f, ensure_ascii=False, indent=4)


#Retrieve details for each steam game
final_game_data = []

for i, game in enumerate(filtered_games[:20000]):  # Limit to the first 20,000 games
    appid = game['appid']
    details_response = requests.get(APP_DETAILS_URL, params={'appids': appid})
    details_data = details_response.json()
    print(appid)
    if details_data and str(appid) in details_data and details_data[str(appid)]['success']:
        game_info = details_data[str(appid)]['data']

        if game_info.get('type') == 'game':  # exclude dlcs, demos,...
            final_game_data.append(game_info)
    
    # avoid overstepping rate limite
    time.sleep(0.1)

with open('final_steam_games.json', 'w') as f:
    json.dump(final_game_data, f, ensure_ascii=False, indent=4)
