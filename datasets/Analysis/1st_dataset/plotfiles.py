import matplotlib.pyplot as plt
import seaborn as sns
import os
import pandas as pd
from wordcloud import WordCloud
from collections import Counter
import string
import re

# Specify the JSON file path
file_path = 'merged_games_final.json'

# Function to load the dataset
def load_dataset(file_path):
    # Load the JSON file
    return pd.read_json(file_path)

# Load the dataset
data = load_dataset(file_path)

# Create a directory to save the plots
output_dir = 'game_analysis_plots_v2'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 1. Price distribution plot
filtered_data = data[data['price'] >= 0.50]
plt.figure(figsize=(10,6))
sns.histplot(filtered_data['price'], bins=30, kde=True)
plt.title("Price Distribution of Games (Not Counting Free To Play)")
plt.xlabel("Price")
plt.ylabel("Frequency")
plt.savefig(os.path.join(output_dir, 'price_distribution.png'))
plt.close()


# 2. NOT INCLUDED Avg Sales distribution plot
plt.figure(figsize=(10,6))
sns.histplot(data['avg_sales'], bins=30, kde=True)
plt.title("Distribution of Average Sales")
plt.xlabel("Average Sales")
plt.ylabel("Frequency")
plt.savefig(os.path.join(output_dir, 'avg_sales_distribution.png'))
plt.close()

# 3. NOT INCLUDED Top 10 Publishers (separate chart)
count_steam_names = data['name'].notna().sum()  
count_ign_reviews = data['ign_review_text'].str.strip().ne('').sum()
count_giantbomb_overviews = data['giantbomb_overview'].str.strip().ne('').sum()
review_counts = {
    'Steam Names': count_steam_names,
    'GiantBomb Overviews': count_giantbomb_overviews,
    'IGN Reviews': count_ign_reviews,
}
count_df = pd.DataFrame(list(review_counts.items()), columns=['Category', 'Count'])
plt.figure(figsize=(8,6))
bars = plt.bar(count_df['Category'], count_df['Count'], color=['darkblue', 'orange', 'red'])
plt.title("Games with Steam Entries, GiantBomb Overviews and IGN Reviews")
plt.ylabel("Number of Games")
plt.xlabel("Category")
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, height, f'{int(height)}', 
             ha='center', va='bottom', fontsize=12, fontweight='bold')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'games_with_reviews.png'))
plt.close()

# 4. IGN Score Distribution
valid_scores = data['ign_score'].replace('', None).astype(float).dropna()
rounded_scores = valid_scores.round().astype(int)
score_counts = rounded_scores.value_counts().reindex(range(1, 11), fill_value=0)
plt.figure(figsize=(10, 6))
bars = plt.bar(score_counts.index, score_counts.values, color='#c21a1a')
plt.title("Distribution of IGN Scores")
plt.ylabel("Number of Games")
plt.xlabel("IGN Scores (Rounded)")
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, height, f'{int(height)}', 
             ha='center', va='bottom', fontsize=12, fontweight='bold')
plt.xticks(score_counts.index)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'ign_score_distribution.png'))
plt.close()

# 5. NOT INCLUDED IGN Review Word Cloud
valid_reviews = data['ign_review_text'].replace('', None).dropna()
stopwords = set([
    'the', 'and', 'or', 'is', 'are', 'has', 'have', 'it', 'of', 'to', 'in', 'that', 'this', 
    'for', 'on', 'with', 'as', 'by', 'an', 'at', 'was', 'from', 'but', 'not', 'be', 'its', 
    'if', 'you', 'can', 'which', 'all', 'about', 'more', 'one', 'just', 'like', 'so', 'we', 
    'they', 'he', 'she', 'their', 'up', 'when', 'there', 'how', 'had', 'out', 'some', 'were',
    'them', 'would', 'could', 'should', 'very', 'into', 'what', 'his', 'her', 'who', 'over',
    'will', 'also', 'than', 'other', 'been', 'only', 'much', 'my', 'your', 'our', 'any', 'most',
    'game', "it's", 'through', 'these', 'while', 'where', 'because', 'being', 'those', 'both',
    'make', 'after', 'before', 'same', 'such', 'many', 'now', 'then', 'well', 'off', 'even',
    "you're", 'i', 'me', 'us', 'him', 'his', 'her', 'she', 'they', 'them', 'their', 'our', 'we',
    'even', 'get', 'got', 'go', 'went', 'come', 'came', 'see', 'saw', 'say', 'said', 'tell', 'told',
    'no', 'yes', 'because', 'why', 'what', 'when', 'where', 'how', 'which', 'who', 'whom', 'whose',
    'do', 'did', 'does', 'done', 'doing', 'make', 'made', 'making', 'take', 'took', 'taking', 'come',
    'such', 'those', 'this', 'that', 'these', 'there', 'here', 'it', 'is', 'are', 'was', 'were', 'be',
    'its', 'youre', 'a', 'still', 'way', 'thats', 'things', 'back', 'never', 'really', 'though', 'few, theyre',
    'often', 'own', 'lot', 'each', 'ways', 'since', 'last', 'two', 'three', 'four', 'five', 'six', 'seven',
    'few', 'found', "don't", 'may', 'might', 'must', 'shall', 'will', 'would', 'should', 'could', 'can',
    'between', 'actually', 'once', 'until', 'getting', 'give', 'across', 'end', 'let', 'along', 'use','too',
    'together', 'means', 'keep', 'makes','set', 'ever', 'start', 'always', 'either', 'kind', 'become', 'without',
    'around', 'thing', 'itself', 'another', 'sometimes', 'having', 'every', 'around', 'whether', 'comes', 'mostly',
    'part', 'takes', 'something', 'gets', 'plenty', 'players'
])
def tokenize_text(text):
    text = text.lower()
    words = text.split()
    words = [word for word in words if word.isalpha() and word not in stopwords]
    return words
all_words = []
for review in valid_reviews:
    words = tokenize_text(review)
    all_words.extend(words)
word_counts = Counter(all_words)
wordcloud = WordCloud(
    width=800, height=400, background_color='white', colormap='plasma'
).generate_from_frequencies(word_counts)
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title("Most Popular Words in IGN Reviews", fontsize=16)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'ign_review_wordcloud.png'))
plt.close()
# 6. NOT INCLUDED Steam Description Word Cloud
valid_steam_descriptions = data['steam_description'].replace('', None).dropna()
all_steam_words = []
for description in valid_steam_descriptions:
    words = tokenize_text(description)
    all_steam_words.extend(words)
steam_word_counts = Counter(all_steam_words)
steam_wordcloud = WordCloud(
    width=800, height=400, background_color='white', colormap='plasma'
).generate_from_frequencies(steam_word_counts)
plt.figure(figsize=(10, 5))
plt.imshow(steam_wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title("Most Popular Words in Steam Descriptions", fontsize=16)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'steam_description_wordcloud.png'))
plt.close()

# 7. NOT INCLUDED Giantbomb Overview Cloud
valid_giantbomb_overviews = data['giantbomb_overview'].replace('', None).dropna()
all_giantbomb_words = []
for overview in valid_giantbomb_overviews:
    words = tokenize_text(overview)
    all_giantbomb_words.extend(words)
giantbomb_word_counts = Counter(all_giantbomb_words)
giantbomb_wordcloud = WordCloud(
    width=800, height=400, background_color='white', colormap='plasma'
).generate_from_frequencies(giantbomb_word_counts)
plt.figure(figsize=(10, 5))
plt.imshow(giantbomb_wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title("Most Popular Words in GiantBomb Overviews", fontsize=16)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'giantbomb_overview_wordcloud.png'))
plt.close()

# Everything Word Cloud
valid_reviews = data['ign_review_text'].replace('', None).dropna()
valid_steam_descriptions = data['steam_description'].replace('', None).dropna()
valid_giantbomb_overviews = data['giantbomb_overview'].replace('', None).dropna()
all_combined_words = []
for review in valid_reviews:
    words = tokenize_text(review)
    all_combined_words.extend(words)
for description in valid_steam_descriptions:
    words = tokenize_text(description)
    all_combined_words.extend(words)
for overview in valid_giantbomb_overviews:
    words = tokenize_text(overview)
    all_combined_words.extend(words)
combined_word_counts = Counter(all_combined_words)
combined_wordcloud = WordCloud(
    width=800, height=400, background_color='white', colormap='plasma'
).generate_from_frequencies(combined_word_counts)
plt.figure(figsize=(10, 5))
plt.imshow(combined_wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title("Most Popular Words Across Steam Descriptions, IGN Reviews and GiantBomb Overviews", fontsize=16)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'combined_wordcloud.png'))
plt.close()

# 5. NOT INCLUDED Top 10 Categories (separate chart)
plt.figure(figsize=(10,6))
common_categories = data['categories'].explode().value_counts().head(10)
common_categories.plot(kind='bar', color='orange')
plt.title("Top 10 Categories")
plt.ylabel("Frequency")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'top_categories.png'))
plt.close()

# 6. NOT INCLUDED Top 10 Genres (separate chart)
plt.figure(figsize=(10,6))
common_genres = data['genres'].explode().value_counts().head(10)
common_genres.plot(kind='bar', color='purple')
plt.title("Top 10 Genres")
plt.ylabel("Frequency")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'top_genres.png'))
plt.close()

# 7. NOT INCLUDED Sales by genre
plt.figure(figsize=(10,6))
genre_sales = data.explode('genres').groupby('genres')['avg_sales'].mean().sort_values(ascending=False)
genre_sales.head(10).plot(kind='bar', color='darkred')
plt.title("Top 10 Game Genres by Average Sales")
plt.xlabel("Genre")
plt.ylabel("Average Sales")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'sales_by_genre.png'))
plt.close()

# NOT INCLUDED Best selling games
plt.figure(figsize=(10,6))
best_selling_games = data[['name', 'avg_sales']].sort_values(by='avg_sales', ascending=False).head(10)
best_selling_games.set_index('name').plot(kind='bar', color='dodgerblue')
plt.title("Top 10 Best-Selling Games")
plt.ylabel("Average Sales")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'best_selling_games.png'))
plt.close()
numeric_columns = ['price', 'avg_sales', 'steam_upvotes', 'steam_downvotes', 'ign_score']
data[numeric_columns] = data[numeric_columns].apply(pd.to_numeric, errors='coerce')
data_cleaned = data.dropna(subset=numeric_columns)

# NOT INCLUDED Common OS support
plt.figure(figsize=(10,6))
common_os = data['os'].explode().value_counts().head(10)
common_os.plot(kind='bar', color='green')
plt.title("Most Common OS Support for Games")
plt.ylabel("Number of Games")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'os_support.png'))
plt.close()

# Most common supported languages
plt.figure(figsize=(10,6))
common_languages = data['supported_languages'].explode().value_counts().head(10)
common_languages.plot(kind='bar', color='darkorange')
plt.title("Most Common Supported Languages in Games")
plt.ylabel("Number of Games")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'supported_languages.png'))
plt.close()

print(f"All plots saved in folder: {output_dir}")
