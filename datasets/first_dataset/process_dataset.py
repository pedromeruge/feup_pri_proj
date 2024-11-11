import json
import re
from datetime import datetime

POPULARITY_THRESHOLD = 100000
END_YEAR = 2022
START_YEAR = 2010
REVIEW_THRESHOLD = 100

def process_dataset(dst_path):
    with open('first_dataset/games.json','r') as games_json:
        games = json.load(games_json)

    parsed_games = remove_unwanted_columns_dataset(games)
    parsed_games = remove_duplicate_entries(parsed_games)
    parsed_games = merge_fields(["categories","tags"],"categories",parsed_games)
    parsed_games = correct_words(["categories"], parsed_games)
    parsed_games = filter_known_games(parsed_games)

    count_games(parsed_games)

    with open(dst_path,'w') as parsed_games_json:
        json.dump(parsed_games, parsed_games_json, ensure_ascii=False, indent=4)

#remove unwanted column fields and filter certain inappropriate games
def remove_unwanted_columns_dataset(games):
    
    unwanted_game_types_filter= re.compile(r'(demo|deluxe|expansion|soundtrack|ost|dlc|vr|beta|pack|trailer|playtest|bundle|artbook|effect|pose|set|tiles|teaser)', re.IGNORECASE)
    explicit_filter = re.compile(r'\b(fuck|sex|porno|xxx|nude|hentai|boobs|fetish|strip|slut|erotic|adult|18+|futanari|femboy|sexy|gay|milf)\b', re.IGNORECASE)
    non_western_characters_filter = re.compile(r'[^\x00-\x7F]+')

    used_fields = [
        'name','required_age','price', 'developers','publishers',
        'categories','genres','supported_languages', 'header_image'
    ]

    #NOTE: although metacritic_score is relevant, most entries had value 0, and metacritic_url is almost never present
    #NOTE: user_score follows the same trend of almost always being 0

    parsed_games = []

    for steam_id,game in games.items():
        if (game['name']
            and not unwanted_game_types_filter.search(game['name'])
            and not explicit_filter.search(game['name'])
            and not non_western_characters_filter.search(game['name'])):
            
                curr_game = {}

                for field in used_fields: # add selected used_fields
                    curr_game[field] = game[field]

                curr_game['steam_description'] = parse_extra_info_in_description(game["detailed_description"]) # if steam api returned more info besides the description, crop it
                if (curr_game['steam_description'] == ""): # if games doesn't have detailed_description, keep the short_description
                    curr_game['steam_description'] = game['short_description']
                curr_game['os'] = [ os for os in ['windows','mac','linux'] if game[os]]
                curr_game['tags'] = list(game['tags'].keys()) if game['tags'] else []
                curr_game['video'] = game['movies'][-1] if game['movies'] else "" # intro video of the steampage if it exists
                curr_game['avg_sales'] = int((int(game["estimated_owners"].split(" - ")[0]) + int(game["estimated_owners"].split(" - ")[1])) / 2) if game["estimated_owners"] else -1 # avg between steamspy estimated min sales and max sales
                curr_game['id'] = steam_id
                curr_game['steam_upvotes'] = game['positive']
                curr_game['steam_downvotes'] = game['negative']

                curr_game['release_date'] =  parse_date(game['release_date']) # split date into Solr’s ISO 8601 format

                parsed_games.append(curr_game)

    return parsed_games

# remove some duplicate entries that exist with the same  name
def remove_duplicate_entries(games):
    
    unique_entries = {}
    #count occurences of names
    for game in games:
        game_name = game['name']
        if (game_name not in unique_entries or 
            (game_name in unique_entries  and game['avg_sales'] > unique_entries[game_name]['avg_sales'])): # if two games with the same name, keep entry with more avg_sales, because the other one is probably the pre-release version
            
            unique_entries[game['name']] = game

    return unique_entries.values()

# merge similar fields, removing duplicate entries
def merge_fields(field_names, final_field_name, games):

    for game in games:
        final_field = set()
        for field in field_names:
            final_field.update(game[field])
            game.pop(field)
        game[final_field_name] = list(final_field)
        game[final_field_name].sort() # sort the results for convenience
    
    return games

#correct certain miss_spelled words in fields
def correct_words(field_names, games):

    normalization_map = { # common wrong spelled words from what we analyzed
        "single-player":"Single-player",
        "single player": "Single-player",
        "singleplayer": "Single-player",
        "cooperative": "Co-op",
        "co-op": "Co-op",
        "multi-player": "Multiplayer",
        "pvp": "PvP"
    }

    for game in games:
        for field in field_names:
            if field in game:
                normalized_entries = set()
                for entry in game[field]:

                    words = entry.split() # split each word in the field, to guarantee individual words are corrected too

                    normalized_words = []

                    for word in words:

                        normalized_word = normalization_map.get(word.lower(), word)
                        normalized_words.append(normalized_word)

                    # merge the words back together
                    normalized_entry = ' '.join(normalized_words)
                    normalized_entries.add(normalized_entry)

            game[field] = sorted(list(normalized_entries))
            game[field]

    return games

#filtering games in relation to release_date and review count
def filter_known_games(games):
    unwanted_categories=['Software','Utilities']
    filtered_games = []

    for game in games:

        release_year = datetime.strptime(game['release_date'], "%Y-%m-%dT%H:%M:%SZ").year

        if (game['avg_sales'] >= POPULARITY_THRESHOLD 
            and release_year >= START_YEAR and release_year <= END_YEAR 
            and (game['steam_upvotes'] + game['steam_downvotes']) >= REVIEW_THRESHOLD
            and not any(category in unwanted_categories for category in game['categories']) # filter out "games" on steam that are actually software, or utility apps
            and not any(genre in unwanted_categories for genre in game['genres'])):
            filtered_games.append(game)

    return filtered_games

# process dates in string format to dictionary format
def parse_date(date_string):
    try:
        # parse full dates like "Jun 4, 2018"
        parsed_date = datetime.strptime(date_string, "%b %d, %Y")
        return parsed_date.strftime("%Y-%m-%dT%H:%M:%SZ")
    except ValueError:
        try:
            # parse partial dates, like format "May 2020"
            parsed_date = datetime.strptime(date_string, "%b %Y")
            # assuming day is the first of the month
            parsed_date = parsed_date.replace(day=1)
            return parsed_date.strftime("%Y-%m-%dT%H:%M:%SZ")
        except ValueError:
            return "Invalid date format"

# some descriptions have additional text at the start, from wrong input in the steam page, that should be removed
def parse_extra_info_in_description(description):
    key_phrase = "About the Game"
    start_index = description.find(key_phrase)
        
    if start_index != -1:
        cropped = description[start_index + len(key_phrase):] 

        return re.sub(r'^[\\/ ]+', '', cropped) # start string after the key_phrase, after any trailing \ or / characters

    #else return original string
    return description

#count games in total
def count_games(games):

    print("total games", len(games))
    # print("games with sale estimates",len([game for game in games if game['avg_sales']]))
    # print("games with date",len([game for game in games if game['release_date']]))
    # print(f"games with sale estimates >= threshold in {START_YEAR}-{END_YEAR}:",len([game for game in games if game['avg_sales'] >= POPULARITY_THRESHOLD and int(game['release_date'].split(" ")[-1]) >= START_YEAR and int(game['release_date'].split(" ")[-1]) <= END_YEAR]))
