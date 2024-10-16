import json
import re
from datetime import datetime

# parse dataset
def process_dataset(src_path, out_path):

    with open(src_path,'r') as games_json:
        data = json.load(games_json)

    parsed_data = fix_missing_values(data)
    parsed_data = merge_fields(["concepts","objects"],"specific_concepts", parsed_data)
    parsed_data = correct_words(["specific_concepts"], parsed_data)

    with open(out_path, 'w') as f:
        json.dump(parsed_data, f, ensure_ascii=False, indent=4)

#fix entries with missing values, or default empty values
def fix_missing_values(data):

    final_data = {}
    for name,game in data.items():
        if not game:
            empty_object = {
                "giantbomb_overview": "",
                "characters": [],
                "locations": [],
                "concepts": [],
                "objects": []
            }
            final_data[name] = empty_object

        else:
            if game['giantbomb_overview'] == "No description":
                game['giantbomb_overview'] = ""
            final_data[name] = game

    return final_data

# merge similar fields, removing duplicate entries
def merge_fields(field_names, final_field_name, games):

    for name, game in games.items():
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

    for name,game in games.items():
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
