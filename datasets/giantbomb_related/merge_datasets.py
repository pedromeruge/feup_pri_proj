import json
import csv

#merges two json datasetes over one specific field, and returns a json dictionary with the key as the merge_field
def merge_initial_dataset_with_giantbomb(first_ds_path, second_ds_path, merge_field, output_path):

    #1st dataset
    with open(first_ds_path,'r') as games_json_1st:
        games_1st = json.load(games_json_1st)

    new_set = set()
    for game in games_1st:
        if game["name"] in new_set:
            print(f"Repeated game {game["name"]}")
        else:
            new_set.add(game["name"])
        
    #2nd dataset
    with open(second_ds_path,'r') as games_json_2nd:
        games_2nd = json.load(games_json_2nd)

    merged_games = {}

    for game_1st in games_1st:
        field = game_1st[merge_field]
        merged_entry = game_1st

        if field in games_2nd:
            merged_entry = {**game_1st, ** games_2nd[field]}
        else:
            print(f"Couldn't merge game: {game_1st["name"]} over field {merge_field}")

        merged_games[field] = merged_entry

    with open(output_path,'w') as merged_games_json:
        json.dump(merged_games, merged_games_json, ensure_ascii=False, indent=4)

    print("Saved", len(merged_games), "merged games")
    return merged_games
