from datasets.config import STEAM_API_KEY

import requests
import time
import json
import csv
import re

# API endpoints
GET_GAME_DETAILS_URL = f'https://www.giantbomb.com/api/games/?api_key=YOUR_API_KEY&format=json&filter=name:' # general list of steam games

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
