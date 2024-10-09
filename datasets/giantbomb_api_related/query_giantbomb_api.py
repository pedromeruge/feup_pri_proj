import sys
import os
import requests
import time

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

source_game_names_file_path = '../2nd_dataset/filtered_games_info.json' # file with game names list, in field 'name', to gather more data about them

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

fetch_games_info()
