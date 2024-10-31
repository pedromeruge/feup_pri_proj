import json

#merges 1st and 2nd dataset, aka 1st_dataset/parsed_games.json with 2nd_dataset/filterd_games_info.json, obtianing one singular more complete dataset
def merge_datasets():
    #1st dataset
    with open('../1st_dataset/parsed_games.json','r') as games_json_1st:
        games_1st = json.load(games_json_1st)
    
    #2nd dataset
    with open('filtered_games_info.json','r') as games_json_2nd:
        games_2nd = json.load(games_json_2nd)

    merged_games = []

    for game_1st in games_1st:
        steam_id = game_1st["steam_id"]
        if steam_id in games_2nd:
            merged_entry = {**game_1st, ** games_2nd[steam_id]}
            merged_games.append(merged_entry)
        else:
            print(f"Couldn't merge game: {game_1st["name"]}")

    with open('merged_games.json','w') as merged_games_json:
        json.dump(merged_games, merged_games_json, ensure_ascii=False, indent=4)

    print("Obtained", len(merged_games), "filtered games")

    merged_games.sort(key=lambda x: x["name"]) # For convenience, sorted games by alphabetical order

merge_datasets()