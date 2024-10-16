import json
import csv

# merges giantbomb and initial games dataset obtained, with the ign reviews dataset, in order to obtain final dataset
def merge_curr_dataset_with_ign_review(json_ds_path, csv_ds_path, merge_field, output_path):

    with open(json_ds_path,'r') as games_json:
        games_1st = json.load(games_json)
    
    with open(csv_ds_path, mode ='r')as games_csv:
        csv_reader = csv.DictReader(games_csv)
        games_2nd = {row[merge_field]: row for row in csv_reader}

    merged_games = []

    merged_count = 0

    for game_name,game_1st in games_1st.items():
        field = game_1st[merge_field]
        merged_entry = game_1st

        if field in games_2nd:
            merged_entry = {**game_1st, **games_2nd[field]}
            merged_count = merged_count + 1

        # else:
        #     print(f"Couldn't merge game {game_name}")

        merged_games.append(merged_entry)

    with open(output_path,'w') as merged_games_json:
        json.dump(merged_games, merged_games_json, ensure_ascii=False, indent=4)

    print("Merged", merged_count, "out of",len(merged_games), "total games")

        