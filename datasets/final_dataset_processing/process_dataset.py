import json

#final processing step, in the dataset
# add missing fields with default value
# remove duplicate entries between categories and specific_concepts
# sort all name lists alphabetically, including the final list
def process_dataset(dataset_path_in, dataset_path_out):

    with open(dataset_path_in,'r') as games_json:
        games = json.load(games_json)

    for game in games:
        # add missing ign_review_text and ign_score fields if they don't exist
        if 'ign_review_text' not in game:
            game['ign_review_text'] = ""
        if 'ign_score' not in game:
            game['ign_score'] = ""

        # remove overlapping values between categories and specific_concepts
        if 'categories' in game and 'specific_concepts' in game:
            categories_set = set(game['categories'])
            game['specific_concepts'] = [concept for concept in game['specific_concepts'] if concept not in categories_set]

        # sort all lists alphabetically (if they exist and are lists)
        for key in ['developers', 'publishers', 'genres', 'supported_languages', 'os', 'categories', 'characters','locations','specific_concepts']:
            game[key].sort()

    with open(dataset_path_out,'w') as merged_games_json:
        json.dump(games, merged_games_json, ensure_ascii=False, indent=4)

    print("Parsed", len(games), "total games")
