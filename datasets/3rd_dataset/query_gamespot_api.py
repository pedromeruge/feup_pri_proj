import os
import sys
import requests
import time
import json
from datetime import datetime

# import gamespot api key from config file
api_key_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(api_key_dir)
from config import GAMESPOT_API_KEY

GET_GAME_REVIEWS_URL = "http://www.gamespot.com/api/reviews/"
RATE_LIMIT = 1 # how long, in seconds???
RETRY_LIMIT = 15 * 60 # wait for 15 minutes if exceeded rate limit

# custom user agent
headers = {
    'User-Agent': 'GetGameReviews (pedrmiguel923@gmail.com)'  # Customize this as needed
}

# save progress of game reviews to a JSON file
def save_progress(final_reviews):
    timestamp = datetime.now().strftime("%d-%H-%M")
    filename = f'results/gamespot_game_reviews_{timestamp}.json'
    with open(filename, 'w') as f:
        json.dump(final_reviews, f, ensure_ascii=False, indent=4)
    print(f"Saved gamespot reviews for {len(final_reviews)} games")

# build the list of games names  we want to find reviews for
def get_game_names_to_obtain_reviews_for():
    with open('../2nd_dataset/merged_games.json','r') as games_json:
        games = json.load(games_json)
    return [game['name'] for game in games][4020:]

#given a game name, finds the corresponding games reviews api url
def fetch_game_reviews_by_title(game_name):

    params = {
        'api_key': GAMESPOT_API_KEY,
        'format': 'json',
        'filter': f'title:{game_name}',  # filter by game name
    }

    response = requests.get(GET_GAME_REVIEWS_URL, params=params, headers=headers)
    if response.status_code == 200:
        data = response.json()
        results = data.get('results', [])
        filtered_reviews = [
            review for review in results 
            if 'game' in review and
            review['game']['name'].lower() == game_name.lower()] # filter only game reviews that actually review that exact game name
        
        return filtered_reviews
        
    elif response.status_code == 420:
        raise Exception("Rate limit exceeded")
    
    else:
        print(f"Error: Received status code {response.status_code} for {game_name}")
        return None

#obtain reviews from gamespot for all games still present in merged_games.json dataset
def fetch_all_games_reviews():
    final_reviews = {}


    games_to_obtain_reviews = get_game_names_to_obtain_reviews_for()
    
    for curr_game_index, game_name in enumerate(games_to_obtain_reviews):
        success = False
        retry_count = 0
        while not success:
            try:
                game_reviews = fetch_game_reviews_by_title(game_name)

                if game_reviews:
                    final_reviews[game_name] = game_reviews
                    print(f"Reviews found for game {game_name}")
                else:
                    print(f"No reviews found for game {game_name}")

                success = True # sucess if obtianed reviews response
                time.sleep(RATE_LIMIT)

            except Exception as e:
                print(f"Error encountered for Game {curr_game_index} ({game_name}): {e}")
                if "Rate limit exceeded" in str(e):
                    print("Rate limit exceeded. Waiting for 15 minutes before retrying...")
                    save_progress(final_reviews)
                    time.sleep(RETRY_LIMIT)
                else:
                    break

    save_progress(final_reviews)

fetch_all_games_reviews()