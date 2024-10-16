import matplotlib.pyplot as plt
import seaborn as sns
import os
import pandas as pd

# Specify the JSON file path
file_path = 'merged_games_final.json'  # Replace with your actual file path

# Function to load the dataset
def load_dataset(file_path):
    # Load the JSON file
    return pd.read_json(file_path)

# Load the dataset
data = load_dataset(file_path)

# Create a directory to save the plots
output_dir = 'game_analysis_plots'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 1. Price distribution plot
plt.figure(figsize=(10,6))
sns.histplot(data['price'], bins=30, kde=True)
plt.title("Price Distribution of Games")
plt.xlabel("Price")
plt.ylabel("Frequency")
plt.savefig(os.path.join(output_dir, 'price_distribution.png'))
plt.close()

# 2. Avg Sales distribution plot
plt.figure(figsize=(10,6))
sns.histplot(data['avg_sales'], bins=30, kde=True)
plt.title("Distribution of Average Sales")
plt.xlabel("Average Sales")
plt.ylabel("Frequency")
plt.savefig(os.path.join(output_dir, 'avg_sales_distribution.png'))
plt.close()

# 3. Top 10 Publishers (separate chart)
plt.figure(figsize=(10,6))
common_publishers = data['publishers'].explode().value_counts().head(10)
common_publishers.plot(kind='bar', color='skyblue')
plt.title("Top 10 Publishers")
plt.ylabel("Number of Games")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'top_publishers.png'))
plt.close()

# 4. Top 10 Developers (separate chart)
plt.figure(figsize=(10,6))
common_developers = data['developers'].explode().value_counts().head(10)
common_developers.plot(kind='bar', color='lightgreen')
plt.title("Top 10 Developers")
plt.ylabel("Number of Games")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'top_developers.png'))
plt.close()

# 5. Top 10 Categories (separate chart)
plt.figure(figsize=(10,6))
common_categories = data['categories'].explode().value_counts().head(10)
common_categories.plot(kind='bar', color='orange')
plt.title("Top 10 Categories")
plt.ylabel("Frequency")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'top_categories.png'))
plt.close()

# 6. Top 10 Genres (separate chart)
plt.figure(figsize=(10,6))
common_genres = data['genres'].explode().value_counts().head(10)
common_genres.plot(kind='bar', color='purple')
plt.title("Top 10 Genres")
plt.ylabel("Frequency")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'top_genres.png'))
plt.close()

# 7. Sales by genre
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

# 8. Best selling games
plt.figure(figsize=(10,6))
best_selling_games = data[['name', 'avg_sales']].sort_values(by='avg_sales', ascending=False).head(10)
best_selling_games.set_index('name').plot(kind='bar', color='dodgerblue')
plt.title("Top 10 Best-Selling Games")
plt.ylabel("Average Sales")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'best_selling_games.png'))
plt.close()

# 9. Handle missing/invalid numeric data before generating the correlation matrix
# Convert columns to numeric and handle non-numeric values
numeric_columns = ['price', 'avg_sales', 'steam_upvotes', 'steam_downvotes', 'ign_score']
data[numeric_columns] = data[numeric_columns].apply(pd.to_numeric, errors='coerce')

# Drop rows with NaN values in the numeric columns
data_cleaned = data.dropna(subset=numeric_columns)

# Generate the correlation matrix
plt.figure(figsize=(10,6))
correlation_matrix = data_cleaned[numeric_columns].corr()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
plt.title("Correlation Heatmap of Selected Features")
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'correlation_heatmap.png'))
plt.close()

# 10. Common OS support
plt.figure(figsize=(10,6))
common_os = data['os'].explode().value_counts().head(10)
common_os.plot(kind='bar', color='green')
plt.title("Most Common OS Support for Games")
plt.ylabel("Number of Games")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'os_support.png'))
plt.close()

# 11. Most common supported languages
plt.figure(figsize=(10,6))
common_languages = data['supported_languages'].explode().value_counts().head(10)
common_languages.plot(kind='bar', color='darkorange')
plt.title("Most Common Supported Languages in Games")
plt.ylabel("Number of Games")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'supported_languages.png'))
plt.close()

# 12. Sizes of description text fields
plt.figure(figsize=(10,6))
data['steam_description_length'] = data['steam_description'].fillna('').apply(len)
data['giantbomb_overview_length'] = data['giantbomb_overview'].fillna('').apply(len)
data['ign_review_text_length'] = data['ign_review_text'].fillna('').apply(len)
data[['steam_description_length', 'giantbomb_overview_length', 'ign_review_text_length']].boxplot()
plt.title("Boxplot of Text Field Sizes")
plt.ylabel("Text Length (characters)")
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'text_field_sizes.png'))
plt.close()

print(f"All plots saved in folder: {output_dir}")
