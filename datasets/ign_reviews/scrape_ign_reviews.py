import requests
from bs4 import BeautifulSoup
import csv

def extract_review_data(url):
    # Add a User-Agent header to the request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'
    }

    response = requests.get(url, headers=headers)
    
    if response.status_code == 403:
        return 'Error 403 - Unavailable', 'Access Blocked', 'Score Not Found'
    
    review_soup = BeautifulSoup(response.content, 'html.parser')

    # Extract the game title from the <h1> tag
    try:
        game_title = review_soup.find('h1').text.strip()
        # Remove "Review" from the end of the title if it's there
        if game_title.split()[-1].lower() == "review":
            game_title = ' '.join(game_title.split()[:-1]).strip()  # Remove the last word
    except AttributeError:
        game_title = 'Title Not Found'

    # Extract the review text from all <p> tags in the page
    try:
        paragraphs = review_soup.find_all('p')
        review_body = ' '.join([p.text.strip() for p in paragraphs if p.text.strip()]).strip()
    except AttributeError:
        review_body = 'Review Not Found'

    # Extract the score (using a broad selector based on your earlier path)
    try:
        score = review_soup.select_one('div.review-score-section figcaption').text.strip()
    except AttributeError:
        score = 'Score Not Found'

    return game_title, review_body, score

# Open the file with the review URLs collected
with open('ign_review_links.txt', 'r') as f:
    review_links = [line.strip() for line in f.readlines()]

# Limit to the first 5 links for testing
review_links = review_links[:2228]  # Only keep the first 5 links for testing

# Open a CSV file to store the scraped review data
with open('ign_reviews.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Game Title', 'Review Text', 'Score'])

    for link in review_links:
        try:
            game, review, score = extract_review_data(link)
            writer.writerow([game, review, score])
            print(f"Scraped review for {game}.")
        except Exception as e:
            print(f"Failed to scrape {link}: {e}")

print("Scraping completed. Data saved to 'ign_reviews.csv'.")





