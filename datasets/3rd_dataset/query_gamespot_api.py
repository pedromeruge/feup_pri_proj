import os
import sys
import requests
import time
import json

# import gamespot api key from config file
api_key_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(api_key_dir)
from config import GAMESPOT_API_KEY

GET_GAME_REVIEWS_URL = "http://www.gamespot.com/api/games/"
RATE_LIMIT = 0.5 # how long, in seconds???

# custom user agent
headers = {
    'User-Agent': 'GetGameReviews (pedrmiguel923@gmail.com)'  # Customize this as needed
}

# save progress of game reviews to a JSON file
def save_progress(final_reviews):

    with open('gamespot_game_reviews.json', 'w') as f:
        json.dump(final_reviews, f, ensure_ascii=False, indent=4)
    print(f"Saved gamespot reviews for {len(final_reviews)} games")

# build the list of games names  we want to find reviews for
def get_game_names_to_obtain_reviews_for():
    with open('../2nd_dataset/merged_games.json','r') as games_json:
        games = json.load(games_json)
    return [game['name'] for game in games]

#given a game name, finds the corresponding games reviews api url
def fetch_game_reviews_api_url(game_name):

    params = {
        'api_key': GAMESPOT_API_KEY,
        'format': 'json',
        'filter': f'name:{game_name}',  # filter by game name,
        'limit': 1  # only need specific game's result
    }

    response = requests.get(GET_GAME_REVIEWS_URL, params=params, headers=headers)
    if response.status_code == 200:
        data = response.json()
        results = data.get('results', [])
        if results:
            # Return the reviews_api_url for the game
            # print(results[0])
            return results[0].get('reviews_api_url', None)
        else:
            print(f"No game found with name {game_name}")
            return None
        
    elif response.status_code == 403:
        raise Exception("Rate limit exceeded")
    
    else:
        print(f"Error: Received status code {response.status_code} for {game_name}")
        return None

# provided a games review url, gets the details of reviews
def fetch_game_reviews_by_url(reviews_api_url):
    params = {
        'api_key': GAMESPOT_API_KEY,
        'format': 'json',
        'limit': 10  # we won't need more than 10 reviews of a game, even if there ar emore
    }

    response = requests.get(reviews_api_url, params=params, headers=headers)
    if response.status_code == 200:
        data = response.json()
        # Extract relevant data from the response
        return data.get('results', [])
    
    elif response.status_code == 403:
        raise Exception("Rate limit exceeded")
    else:
        print(f"Error: Received status code {response.status_code} for {reviews_api_url}")
        return None

#obtain reviews from gamespot for all games still present in merged_games.json dataset
def fetch_all_games_reviews():
    final_reviews = {}

    games_to_obtain_reviews = get_game_names_to_obtain_reviews_for()
    
    for curr_game_index, game_name in enumerate(games_to_obtain_reviews):
        try:
            game_reviews_api_url = fetch_game_reviews_api_url(game_name)
            if game_reviews_api_url:
                print("review_url: ", game_reviews_api_url)
                game_reviews = fetch_game_reviews_by_url(game_reviews_api_url)

                if game_reviews:
                    final_reviews[game_name] = game_reviews
                    print(f"Reviews found for game {game_name}")
                else:
                    print(f"No reviews found for game {game_name}")

            time.sleep(RATE_LIMIT)

        except Exception as e:
            print(f"Error encountered for Game {curr_game_index} ({game_name}): {e}")
            save_progress(final_reviews)
            break # stop loop if limit rate exceeded

    save_progress(final_reviews)

fetch_all_games_reviews()