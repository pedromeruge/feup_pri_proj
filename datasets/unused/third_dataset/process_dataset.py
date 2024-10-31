import json
from bs4 import BeautifulSoup
from datetime import datetime

def main():
    with open('game_reviews.json','r') as game_reviews:
        reviews = json.load(game_reviews)

    reviews = remove_unwanted_columns(reviews)
    reviews = remove_duplicate_entries(reviews)

    with open('parsed_game_reviews.json','w') as parsed_game_reviews:
        json.dump(reviews, parsed_game_reviews, ensure_ascii=False, indent=4)

    print("Obtained", len(reviews), "parsed reviews")

def filter_html_from_text(html_text):
    soup = BeautifulSoup(html_text, "html.parser")
    final_text = soup.get_text(separator="") # substitute tags with spaces. Should be what was intended?

    return final_text.strip()

def remove_unwanted_columns(game_reviews):

    parsed_reviews = {}

    for name, reviews in game_reviews.items():
        review_list = []

        for review  in reviews:
            curr_game = {}
            
            curr_game['date'] = review['update_date']
            curr_game['authors'] = review['authors']
            curr_game['final_score'] = float(review['score'])
            curr_game['text_review'] = filter_html_from_text(review['body'])
            curr_game['good'] = review['good']
            curr_game['bad'] = review['bad']

            review_list.append(curr_game)

        parsed_reviews[name] = review_list
    
    return parsed_reviews

# remove entries where a certain author publishes consecutive reviews with minimal differences, fetch only the latest one
def remove_duplicate_entries(game_reviews):
    final_reviews = {}
    for name, reviews in game_reviews.items():
        filtered_results = {}
        for entry in reviews:
            key = (entry['authors']) # only include the latest reviews by an author, if he has many reviews on the same game

            if key not in filtered_results or parse_date(entry['date']) > parse_date(filtered_results[key]['date']):
                filtered_results[key] = entry
        
        final_reviews[name] = list(filtered_results.values())

    return final_reviews

def parse_date(date):
    return datetime.strptime(date, "%Y-%m-%d %H:%M:%S")

main()