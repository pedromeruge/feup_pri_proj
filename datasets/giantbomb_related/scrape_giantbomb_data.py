import requests
from bs4 import BeautifulSoup
import time
import json

RATE_LIMIT = 0.5

#scrape additional data of overview, characters,locations, concepts, objects for games found inside src_path
def scrape(src_path, dst_path):

    game_names = get_game_names_to_obtain_info_for(src_path)
    data = scrape_game_data_from_game_names(game_names)

    with open(dst_path, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# build the list of games names we want to find extra info for
def get_game_names_to_obtain_info_for(src_path):
    with open(src_path,'r') as games_json:
        games = json.load(games_json)
    return [game['name'] for game in games]

#find game's description page url, provided its name
def search_game(game_name):
    search_url = f"https://www.giantbomb.com/search/?i=game&q={game_name.replace(' ', '+')}"
    response = requests.get(search_url)
    
    if response.status_code != 200:
        print(f"Failed to search results for {game_name}.")
        return None
    
    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # find first game's url in list of search results
    first_result = soup.find('ul', id='js-sort-filter-results')

    if not first_result:
        print(f"No search results found for {game_name}")
        return None
    
    href_result = first_result.find('a',href=True)
    title_result = first_result.find('h3',class_='title')
    title_tag = title_result.get_text(strip=True).lower() if title_result else None

    if href_result and title_tag == game_name.strip().lower(): # check if any result, and if there is a result it is the correct name
        game_url = "https://www.giantbomb.com" + href_result['href']
        return game_url
    else:
        print(f"Game found, but title does not match")
        return None

# Scrape the main content from the game page
def scrape_game_page(game_url):
    response = requests.get(game_url)
    if response.status_code != 200:
        print(f"Failed to fetch game page: {game_url}")
        return None
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Scrape the game description from the wiki section
    wiki_section = soup.find('div', class_='wiki-item-display js-toc-content')
    
    if wiki_section:
        for header in wiki_section.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'figcaption']):
            header.decompose()  # remove headers and figure captions from text

        # get only the text inside all the remaining divs, and substitute tags for spaces
        game_description = wiki_section.get_text(separator=' ', strip=True)
        return game_description
    else:
        print("No description found on the game page.")
        return None

# scrape extra info of the game realted to characters, locations, concepts, ...
def scrape_additional_info_page(game_url, extra_url_endpoint):
    extra_url = game_url + extra_url_endpoint
    return scrape_multiple_pages(extra_url, 'div', 'primary-content js-article-container span8')

# scrape multiple pages (for characters or other paginated sections)
def scrape_multiple_pages(url, tag, class_name):
    page = 1
    all_titles = []
    
    while True:
        current_url = f"{url}?page={page}"
        response = requests.get(current_url)
        
        if response.status_code != 200:
            print(f"Failed to fetch page {page}: {current_url}")
            break
        
        soup = BeautifulSoup(response.text, 'html.parser')
        objective_section = soup.find(tag, class_=class_name)
        
        if not objective_section:
            print(f"No more content found on page {page}",end="")
            break
        
        # extract titles of the enumerated elements in the page
        titles = objective_section.find_all('h3', class_='title')
        all_titles.extend(title.get_text(strip=True) for title in titles)
        
        # check for next page
        next_page_item = soup.find('li', class_='skip next')

        if not next_page_item:
            # print(f"(pages 1-{page})")
            break

        # Construct the next page URL
        page += 1
        time.sleep(RATE_LIMIT)

    return all_titles

# scrape all data related to a game: page description, characters, locations, concepts, objects
def scrape_game_data(game_name):
    game_url = search_game(game_name)
    
    game_data = {}
    if game_url:
        print(f"Found game {game_name}")
        
        # scrape game description
        game_data["giantbomb_overview"] = scrape_game_page(game_url)

        # if game_data["giantbomb_text"]:
        #     print(f">>Found game description")

        # scrape extra topics
        extra_pages_info = ["characters","locations","concepts","objects"]

        for page in extra_pages_info:
            game_data[page] = scrape_additional_info_page(game_url, page)
            # if game_data[page]:
                # print(f">>Found games {page}")
    else:
        print(f"Could not find {game_name} URL")

    return game_data

# 
def scrape_game_data_from_game_names(game_names_list):
    total_len = len(game_names_list)
    results = {}
    for i, game_name in enumerate(game_names_list):
        results[game_name] = scrape_game_data(game_name)
        print(f"[{i+1}/{total_len}] done")
    return results
