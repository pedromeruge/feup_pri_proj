import sys
import os
import requests
import time
from datetime import datetime
import json

# import config file for api key
api_key_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(api_key_dir)
from config import GIANTBOMB_API_KEY

# API endpoints
GET_GAME_DETAILS_URL = f'https://www.giantbomb.com/api/games/?api_key={GIANTBOMB_API_KEY}&format=json&resource=game' # details of game, including id
GET_CHARACTERS_URL = f'https://www.giantbomb.com/api/characters/?api_key={GIANTBOMB_API_KEY}&format=json&field_list=name'
GET_LOCATIONS_URL = f'https://www.giantbomb.com/api/locations/?api_key={GIANTBOMB_API_KEY}&format=json&field_list=name'
GET_CONCEPTS_URL = f'https://www.giantbomb.com/api/concepts/?api_key={GIANTBOMB_API_KEY}&format=json&field_list=name'
GET_OBJECTS_URL = f'https://www.giantbomb.com/api/objects/?api_key={GIANTBOMB_API_KEY}&format=json&field_list=name'

RATE_LIMIT = 0.5
RETRY_LIMIT = 20 * 60 # wait for 45 minutes if exceeded rate limit

source_game_names_file_path = '../1nd_dataset/parsed_games.json' # file with game names list, in field 'name', to gather more data about them

# custom user agent
headers = {
    'User-Agent': 'GetGameDetails/1.0 (pedrmiguel923@gmail.com)'  # Customize this as needed
}

def get_game_by_name(game_name):

    response = requests.get(GET_GAME_DETAILS_URL, params={'filter': f'name:{game_name}'}, headers=headers)
    if response.status_code != 200:
        print(f"Error fetching game details: {response.status_code} - {response.text}")
        return []

    try:
        data = response.json()
    except json.JSONDecodeError:
        print("Error decoding JSON response:", response.text)
        return []

    return data.get('results', [])


def get_associated_entity_names(game_name):
    associated_data = {
        'characters': [],
        'locations': [],
        'concepts': [],
        'objects': []
    }
    
    # character names
    characters_response = requests.get(GET_CHARACTERS_URL, params={'filter':f'games:{game_name}'}, headers=headers)
    if characters_response.status_code == 200:
        characters = characters_response.json().get('results', [])
        associated_data['characters'] = [character['name'] for character in characters]

    # Fetch locations associated with the game name
    locations_response = requests.get(GET_LOCATIONS_URL, params={'filter':f'games:{game_name}'}, headers=headers)
    if locations_response.status_code == 200:
        locations = locations_response.json().get('results', [])
        associated_data['locations'] = [location['name'] for location in locations]

    # Fetch concepts associated with the game name
    concepts_response = requests.get(GET_CONCEPTS_URL, params={'filter':f'games:{game_name}'}, headers=headers)
    if concepts_response.status_code == 200:
        concepts = concepts_response.json().get('results', [])
        associated_data['concepts'] = [concept['name'] for concept in concepts]

    # Fetch objects associated with the game name
    objects_response = requests.get(GET_OBJECTS_URL, params={'filter':f'games:{game_name}'}, headers=headers)
    if objects_response.status_code == 200:
        objects = objects_response.json().get('results', [])
        associated_data['objects'] = [obj['name'] for obj in objects]
    
    return associated_data

def fetch_games_info():
    with open(source_game_names_file_path, 'r') as f:
        games = json.load(f)

    final_game_data = []

    for game in games:  # Adjust the slice as needed
        game_data = get_game_by_name(game['name'])
        
        if game_data and game_data[0]['name'].lower() == game['name'].lower(): # if exact match is found

        #     game_name = game_data[0]['name']

            print(game_data[0]['id'], game_data[0]['name'])

        #     associated_entity_names = get_associated_entity_names(game_name)
        #     final_game_data.append({
        #         'game': game_data[0]['name'],  # Store only the game name
        #         'associated_entities': associated_entity_names
        #     })
        
            final_game_data.append(game_data[0])

        time.sleep(1)  # Respect rate limits

    with open('giantbomb_games.json', 'w') as f:
        json.dump(final_game_data, f, ensure_ascii=False, indent=4)

def fetch_all_games_info_between_dates(start_date, end_date):
    
    response_limit = 100 # max values returned by API per request
    games_info = []
    offset = 17500

    while True:
        params = {
            'filter': f'original_release_date:{start_date} 000:00:00|{end_date} 000:00:00',
            'sort': 'original_release_date:asc',
            'field_list': 'id,name,original_release_date,site_detail_url',
            'offset': offset
        }

        response = requests.get(GET_GAME_DETAILS_URL, params=params, headers=headers)
        
        data = response.json()

        if response.status_code == 420: #pause if we hit the request limit

            print(f"Fetched {len(games_info)} games. Current offset: {offset}. Sleeping for {RETRY_LIMIT} minutes...")
            save_progress(games_info)
            
            time.sleep(RETRY_LIMIT)

        elif response.status_code != 200 or int(data["number_of_total_results"]) == 0:
            print(f"Error fetching game details: {response.status_code} - {response.text}")
            print(f"Offset: {offset}")
            save_progress(games_info)
            return

        else:
            games = data.get('results', [])

            # add fetched games to list
            games_info.extend(games)

            
            # stop if we've reached the last page (less than the limit of games is returned)
            if int(data["offset"]) + int(data["limit"]) >= int(data["number_of_total_results"]): # if we get less than 100 games, we've reached the end of the list
                break

            print(f"Fetched {data["number_of_page_results"]} results in offset {offset}")
            offset += response_limit

            time.sleep(RATE_LIMIT)
    
    save_progress(games_info)
    print("Fetched all available games within the date range.")

#save current data fetched to a file
def save_progress(data):
    timestamp = datetime.now().strftime("%d-%H-%M")
    filename = f'results/giantbomb_game_data_{timestamp}.json'
    with open(filename, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Saved giantbomb data for {len(data)} games")

fetch_all_games_info_between_dates("2013-01-01","2022-12-31")
