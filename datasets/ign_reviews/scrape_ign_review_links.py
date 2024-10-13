from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

# Set up Chrome options (optional headless mode)
chrome_options = Options()
chrome_options.add_argument("--headless")  # Optional: run headless
chrome_options.add_argument("--no-sandbox")

# Specify the path to your chromedriver binary
service = Service(r'C:\Users\anton\chromedriver\chromedriver.exe')

# Initialize the Chrome WebDriver
driver = webdriver.Chrome(service=service, options=chrome_options)

# Go to the specific page for PC game reviews
driver.get('https://www.ign.com/reviews/games/pc')

# Scroll down the page to load more reviews (infinite scrolling)
SCROLL_PAUSE_TIME = 2  # Pause time for content to load
IGNORE_LINKS = 2078     # Number of links to ignore
MAX_LINKS = 150        # Number of links to collect after ignoring
review_links = []
last_height = driver.execute_script("return document.body.scrollHeight")

# Skip the first IGNORE_LINKS links
while len(review_links) < IGNORE_LINKS:
    # Parse the current page source
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Find and collect game review links
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        
        # Only collect article links that likely contain reviews
        if '/articles/' in href and 'review' in href:
            full_url = 'https://www.ign.com' + href if not href.startswith('http') else href
            if full_url not in review_links:
                review_links.append(full_url)
                if len(review_links) >= IGNORE_LINKS:  # Check if we reached the limit
                    break

    # Scroll down to the bottom of the page
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait for new content to load
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")

    if new_height == last_height:
        print("No more content to load.")
        break
    last_height = new_height

print(f"Ignored the first {IGNORE_LINKS} links. Now collecting the next {MAX_LINKS} links.")

# Collect the next MAX_LINKS (500) after ignoring the first IGNORE_LINKS (1000)
while len(review_links) < IGNORE_LINKS + MAX_LINKS:
    # Parse the current page source
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Find and collect game review links
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        
        # Only collect article links that likely contain reviews
        if '/articles/' in href and 'review' in href:
            full_url = 'https://www.ign.com' + href if not href.startswith('http') else href
            if full_url not in review_links:
                review_links.append(full_url)
                if len(review_links) >= IGNORE_LINKS + MAX_LINKS:  # Check if we reached the total limit
                    break

    # Scroll down to the bottom of the page
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait for new content to load
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")

    if new_height == last_height:
        print("No more content to load.")
        break
    last_height = new_height

# Save the collected game review links to a file
with open('ign_pc_review_links.txt', 'w') as f:
    for link in review_links:
        f.write(link + '\n')

print(f"Found {len(review_links) - IGNORE_LINKS} new game review links. Links saved to 'ign_pc_review_links.txt'.")

# Close the browser
driver.quit()

