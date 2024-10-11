import json
import re
from datetime import datetime

POPULARITY_THRESHOLD = 100000
END_YEAR = 2022
START_YEAR = 2013

def main():
    with open('games.json','r') as games_json:
        games = json.load(games_json)

    parsed_games = remove_unwanted_columns_dataset(games)
    # parsed_games = filter_known_games(parsed_games)

    count_games(parsed_games)

    with open('parsed_games.json','w') as parsed_games_json:
        json.dump(parsed_games, parsed_games_json, ensure_ascii=False, indent=4)

#remove unwanted column fields and filter certain inappropriate games
def remove_unwanted_columns_dataset(games):
    
    unwanted_game_types_filter= re.compile(r'(demo|deluxe|expansion|soundtrack|ost|dlc|vr|beta|pack|trailer|playtest|bundle|artbook|effect|pose|set|tiles|teaser)', re.IGNORECASE)
    explicit_filter = re.compile(r'\b(fuck|sex|porno|xxx|nude|hentai|boobs|fetish|strip|slut|erotic|adult|18+|futanari|femboy|sexy|gay|milf)\b', re.IGNORECASE)
    non_western_characters_filter = re.compile(r'[^\x00-\x7F]+')

    used_fields = [
        'name','release_date','required_age','price','dlc_count','short_description','detailed_description',
        'header_image','developers','publishers','categories','genres','supported_languages'
    ]

    parsed_games = []

    for steam_id,game in games.items():
        if (game['name']
            and not unwanted_game_types_filter.search(game['name'])
            and not explicit_filter.search(game['name'])
            and not non_western_characters_filter.search(game['name'])):
            
                curr_game = {}

                for field in used_fields: # add selected used_fields
                    curr_game[field] = game[field]
                curr_game['os'] = [ os for os in ['windows','mac','linux'] if game[os]]
                curr_game['tags'] = list(game['tags'].keys()) if game['tags'] else []
                curr_game['video'] = game['movies'][-1] if game['movies'] else [] # intro video of the steampage
                curr_game['avg_sales'] = int((int(game["estimated_owners"].split(" - ")[0]) + int(game["estimated_owners"].split(" - ")[1])) / 2) if game["estimated_owners"] else -1 # avg between steamspy estimated min sales and max sales
                curr_game['steam_id'] = steam_id
                curr_game['positive_reviews'] = game['positive']
                curr_game['negative_reviews'] = game['negative']

                parsed_games.append(curr_game)

    return parsed_games

#filtering games from 2013-2023
#filtering games with x >= amount of units sold
def filter_known_games(games):
    filtered_games = []

    for game in games:

        release_year = int(game['release_date'].split(" ")[-1])

        if game['avg_sales'] >= POPULARITY_THRESHOLD and release_year >= START_YEAR and release_year <= END_YEAR:
            filtered_games.append(game)

    return filtered_games


#count games in total, with sale estimates, and above a certain sale threshold amount
def count_games(games):

    print("total games", len(games))
    print("games with sale estimates",len([game for game in games if game['avg_sales']]))
    print("games with date",len([game for game in games if game['release_date']]))
    print("games with sale estimates >= threshold",len([game for game in games if game['avg_sales'] >= POPULARITY_THRESHOLD]))
main()