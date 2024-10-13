import json
import sys 

#merges two datasetes over one specific field
def merge_datasets(first_ds_path, second_ds_path, merge_field, output_path):
    #1st dataset
    with open(first_ds_path,'r') as games_json_1st:
        games_1st = json.load(games_json_1st)
    
    #2nd dataset
    with open(second_ds_path,'r') as games_json_2nd:
        games_2nd = json.load(games_json_2nd)

    merged_games = []

    for game_1st in games_1st:
        field = game_1st[merge_field]
        if field in games_2nd:
            merged_entry = {**game_1st, ** games_2nd[field]}
            merged_games.append(merged_entry)
        else:
            print(f"Couldn't merge game: {game_1st["name"]} over field {merge_field}")

    merged_games.sort(key=lambda x: x["name"]) # For convenience, sorted games by alphabetical order
    
    with open(output_path,'w') as merged_games_json:
        json.dump(merged_games, merged_games_json, ensure_ascii=False, indent=4)

    print("Saved", len(merged_games), "merged games")
    return merged_games
