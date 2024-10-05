import json
import re

def process_dataset():
    with open('games.json','r') as games_json:
        games = json.load(games_json)

    unwanted_game_types_filter= re.compile(r'(demo|deluxe|expansion|soundtrack|ost|dlc|vr|beta|pack|trailer|playtest|bundle|artbook|effect|pose|set|tiles|teaser)', re.IGNORECASE)
    explicit_filter = re.compile(r'\b(fuck|sex|porno|xxx|nude|hentai|boobs|fetish|strip|slut|erotic|adult|18+|futanari|femboy|sexy)\b', re.IGNORECASE)
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
                curr_game['min_sales'] = game["estimated_owners"].split(" - ")[0] # steamspy estimated min sales
                curr_game['max_sales'] = game["estimated_owners"].split(" - ")[1] # steamspy estimated max sales
                curr_game['steam_id'] = steam_id
                curr_game['positive_reviews'] = game['positive']
                curr_game['negative_reviews'] = game['negative']

                parsed_games.append(curr_game)


    with open('parsed_games.json','w') as parsed_games_json:
        json.dump(parsed_games, parsed_games_json, ensure_ascii=False, indent=4)

    print("Obtained", len(parsed_games), "parsed games")

process_dataset()