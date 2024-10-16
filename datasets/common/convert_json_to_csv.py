import json
import pandas as pd

# Module to load json data into csv, to be able to analyize in rapidminer
#load json data

def convert_parsed_games_to_csv():
    source_file_path = 'first_dataset/parsed_games.json'
    dest_file_path = 'first_dataset/parsed_games.csv'
    with open(source_file_path,'r') as json_file:
        data = json.load(json_file)

    processed_data = []

    for game in data:
        flat_game = {
            "name": game["name"],
            "required_age": game["required_age"],
            "price": game["price"],
            "steam_description": game["steam_description"],
            "developers": ';'.join(game["developers"]),  
            "publishers": ';'.join(game["publishers"]),  
            "categories": ';'.join(game["categories"]),  
            "genres": ';'.join(game["genres"]),        
            "supported_languages": ';'.join(game["supported_languages"]),
            "header_image": game["header_image"],
            "os": ';'.join(game["os"]),                        
            "avg_sales": game["avg_sales"],
            "steam_upvotes": game["steam_upvotes"],
            "steam_downvotes": game["steam_downvotes"],
            "release_date_day": game["release_date"]["day"],
            "release_date_month": game["release_date"]["month"],
            "release_date_year": game["release_date"]["year"],
        }
        
        processed_data.append(flat_game)

    df = pd.DataFrame(processed_data)

    # Export to CSV
    df.to_csv(dest_file_path, index=False)

def convert_orig_games_dataset_to_csv():
    source_file_path = 'first_dataset/games.json'
    dest_file_path = 'first_dataset/games.csv'
    with open(source_file_path,'r') as json_file:
        data = json.load(json_file)

    processed_data = []

    for game in data.values():
        if game and game["name"]:
            flat_game = {
                "name": game["name"],
                "required_age": game["required_age"],
                "price": game["price"],
                "description": game["detailed_description"],
                "developers": ';'.join(game["developers"]),  
                "publishers": ';'.join(game["publishers"]),  
                "categories": ';'.join(game["categories"]),  
                "genres": ';'.join(game["genres"]),        
                "supported_languages": ';'.join(game["supported_languages"]),
                "header_image": game["header_image"],           
                "tags": ';'.join(game["tags"]),            
                "estimated_sales": game["estimated_owners"],
                "steam_upvotes": game["positive"],
                "steam_downvotes": game["negative"],
                "release_date": game["release_date"],
                "metacritic_score": game["metacritic_score"] if game["metacritic_score"] else -1,
                "metacritic_url": game["metacritic_url"] if game["metacritic_url"] else "",
                "user_score": game["user_score"] if game["user_score"] else -1
            }
        
        processed_data.append(flat_game)

    df = pd.DataFrame(processed_data)

    # Export to CSV
    df.to_csv(dest_file_path, index=False)

convert_parsed_games_to_csv()