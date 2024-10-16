import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
data = pd.read_json('merged_games_final.json')

# 1. Key Features and Dataset Overview
print(data.info())
print(data.head())

# 2. Numerical Analysis
data['ign_score_numeric'] = pd.to_numeric(data['ign_score'], errors='coerce')
numerical_columns = ['price', 'avg_sales', 'steam_upvotes', 'steam_downvotes', 'ign_score_numeric']
print(data[numerical_columns].describe())

# 3. Price Distribution
plt.figure(figsize=(10, 6))
plt.hist(data['price'], bins=30, color='blue', edgecolor='black')
plt.title('Price Distribution')
plt.xlabel('Price (USD)')
plt.ylabel('Frequency')
plt.grid(True)
plt.show()

# 4. Avg Sales Distribution
plt.figure(figsize=(10, 6))
plt.hist(data['avg_sales'], bins=30, color='green', edgecolor='black', log=True)  # Log scale for visibility
plt.title('Distribution of Average Sales')
plt.xlabel('Average Sales')
plt.ylabel('Frequency (Log Scale)')
plt.grid(True)
plt.show()

# 5. Frequency of Games by Release Year
data['release_year'] = data['release_date'].apply(lambda x: x['year'] if x and 'year' in x else None)
plt.figure(figsize=(10, 6))
data['release_year'].value_counts().sort_index().plot(kind='bar', color='skyblue')
plt.title('Frequency of Game Releases by Year')
plt.xlabel('Year')
plt.ylabel('Number of Games Released')
plt.grid(True)
plt.show()

# 6. Common Publishers, Developers, Categories, Genres
exploded_publishers = data.explode('publishers')
exploded_developers = data.explode('developers')
exploded_categories = data.explode('categories')
exploded_genres = data.explode('genres')

# Top Publishers
plt.figure(figsize=(10, 6))
exploded_publishers['publishers'].value_counts().head(10).plot(kind='bar', color='green')
plt.title('Top 10 Publishers')
plt.xlabel('Publisher')
plt.ylabel('Number of Games')
plt.grid(True)
plt.show()

# Top Developers
plt.figure(figsize=(10, 6))
exploded_developers['developers'].value_counts().head(10).plot(kind='bar', color='orange')
plt.title('Top 10 Developers')
plt.xlabel('Developer')
plt.ylabel('Number of Games')
plt.grid(True)
plt.show()

# Top Categories
plt.figure(figsize=(10, 6))
exploded_categories['categories'].value_counts().head(10).plot(kind='bar', color='purple')
plt.title('Top 10 Categories')
plt.xlabel('Category')
plt.ylabel('Number of Games')
plt.grid(True)
plt.show()

# Top Genres
plt.figure(figsize=(10, 6))
exploded_genres['genres'].value_counts().head(10).plot(kind='bar', color='blue')
plt.title('Top 10 Genres')
plt.xlabel('Genre')
plt.ylabel('Number of Games')
plt.grid(True)
plt.show()

# 7. Best-Selling Games
top_selling_games = data[['name', 'avg_sales']].sort_values(by='avg_sales', ascending=False).head(10)
print(top_selling_games)

# 8. Correlation Heatmap
numerical_data = data[['price', 'avg_sales', 'steam_upvotes', 'steam_downvotes', 'ign_score_numeric']]
correlation_matrix = numerical_data.corr()

plt.figure(figsize=(8, 6))
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", linewidths=0.5)
plt.title('Correlation Heatmap')
plt.show()

# 9. Common OS Support
exploded_os = data.explode('os')
plt.figure(figsize=(10, 6))
exploded_os['os'].value_counts().head(10).plot(kind='bar', color='cyan')
plt.title('Top 10 Supported Operating Systems')
plt.xlabel('Operating System')
plt.ylabel('Number of Games')
plt.grid(True)
plt.show()

# 10. Common Supported Languages
exploded_languages = data.explode('supported_languages')
plt.figure(figsize=(10, 6))
exploded_languages['supported_languages'].value_counts().head(10).plot(kind='bar', color='red')
plt.title('Top 10 Supported Languages')
plt.xlabel('Supported Language')
plt.ylabel('Number of Games')
plt.grid(True)
plt.show()

# 11. Games with IGN Reviews, Scores, Characters, Locations, Concepts
ign_reviews_count = data['ign_review_text'].apply(lambda x: 1 if x.strip() else 0).sum()
ign_score_count = data['ign_score'].apply(lambda x: 1 if x.strip() else 0).sum()
characters_count = data['characters'].apply(lambda x: 1 if x else 0).sum()
locations_count = data['locations'].apply(lambda x: 1 if x else 0).sum()
concepts_count = data['specific_concepts'].apply(lambda x: 1 if x else 0).sum()
giantbomb_overview_count = data['giantbomb_overview'].apply(lambda x: 1 if x else 0).sum()

summary_data = {
    'IGN Reviews Text': ign_reviews_count,
    'IGN Score': ign_score_count,
    'Characters': characters_count,
    'Locations': locations_count,
    'Concepts': concepts_count,
    'Giantbomb Overview': giantbomb_overview_count
}
summary_df = pd.DataFrame(list(summary_data.items()), columns=['Feature', 'Count'])
print(summary_df)

# 12. Text Field Sizes
data['steam_description_length'] = data['steam_description'].apply(len)
data['giantbomb_overview_length'] = data['giantbomb_overview'].apply(lambda x: len(x) if isinstance(x, str) else 0)
data['ign_review_text_length'] = data['ign_review_text'].apply(len)

# Plotting histograms for text field sizes
plt.figure(figsize=(12, 8))

plt.subplot(3, 1, 1)
plt.hist(data['steam_description_length'], bins=30, color='lightblue')
plt.title('Steam Description Lengths')
plt.xlabel('Number of Characters')
plt.ylabel('Frequency')

plt.subplot(3, 1, 2)
plt.hist(data['giantbomb_overview_length'], bins=30, color='lightgreen')
plt.title('Giantbomb Overview Lengths')
plt.xlabel('Number of Characters')
plt.ylabel('Frequency')

plt.subplot(3, 1, 3)
plt.hist(data['ign_review_text_length'], bins=30, color='lightcoral')
plt.title('IGN Review Text Lengths')
plt.xlabel('Number of Characters')
plt.ylabel('Frequency')

plt.tight_layout()
plt.show()

# 13. Sales by Release Year
sales_by_year = data.groupby('release_year')['avg_sales'].sum().sort_index()
plt.figure(figsize=(12, 6))
sales_by_year.plot(kind='bar', color='skyblue')
plt.title('Total Game Sales by Release Year')
plt.xlabel('Release Year')
plt.ylabel('Total Sales')
plt.grid(True)
plt.show()
