import json
import re

IGDB_POPULARITY_MIN = 1.01

#after running process_dataset.py script, these script filters only the most relevant games accoriding to igdb, to obtain a subset of the data
def filter_relevant_games_dataset():
    with open('parsed_games_info.json','r') as games_json:
        games = json.load(games_json)

    filtered_games = {}

    for steam_id, game in games.items():
        if game['igdb_popularity'] and game['igdb_popularity'] >= IGDB_POPULARITY_MIN:
            filtered_games[steam_id] = game

    with open('filtered_games_info.json','w') as parsed_games_json:
        json.dump(filtered_games, parsed_games_json, ensure_ascii=False, indent=4)

    print("Obtained", len(filtered_games), "filtered games")

filter_relevant_games_dataset()