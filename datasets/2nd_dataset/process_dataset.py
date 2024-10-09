import json
import re

def process_dataset():
    with open('games_info/games_info.json','r') as games_json:
        games = json.load(games_json)

    unwanted_game_types_filter= re.compile(r'(demo|deluxe|expansion|soundtrack|ost|dlc|vr|beta|pack|trailer|playtest|bundle|artbook|effect|pose|set|tiles|teaser)', re.IGNORECASE)
    explicit_filter = re.compile(r'\b(fuck|sex|porno|xxx|nude|hentai|boobs|fetish|strip|slut|erotic|adult|18+|futanari|femboy|sexy|gay|milf)\b', re.IGNORECASE)
    non_western_characters_filter = re.compile(r'[^\x00-\x7F]+')

    used_fields = [
        'name','igdb_score','igdb_uscore','igdb_popularity'
    ]

    parsed_games = {}

    for game in games:
        game['name'] = str(game['name'])
        if (game['name']
            and not unwanted_game_types_filter.search(game['name'])
            and not explicit_filter.search(game['name'])
            and not non_western_characters_filter.search(game['name'])):
            
                curr_game = {}

                curr_game['gamefaqs_rating'] = game['gfq_rating']
                curr_game['metacritic_score'] = game['meta_score']
                curr_game['metacrtic_uscore'] = game['meta_uscore']
                for field in used_fields:
                    curr_game[field] = game[field]
                
                parsed_games[game['sid']] = curr_game

    with open('parsed_games_info.json','w') as parsed_games_json:
        json.dump(parsed_games, parsed_games_json, ensure_ascii=False, indent=4)

    print("Obtained", len(parsed_games), "parsed games")

process_dataset()