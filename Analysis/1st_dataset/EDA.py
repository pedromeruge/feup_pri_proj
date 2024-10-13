import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

# Step 1: Load the JSON file
json_file_path = 'parsed_games.json'  # Replace with the actual path to your file
df = pd.read_json(json_file_path)

# Step 2: Basic Inspection
print("First 5 rows of the dataset:")
print(df.head())
print("\nDataset Information:")
print(df.info())

# Step 3: Descriptive Statistics for numerical columns
print("\nDescriptive statistics for numerical columns:")
print(df.describe())

# Step 4: Check for Missing Data
print("\nMissing data in each column:")
print(df.isnull().sum())

# Step 5: Visualizations

# Price Distribution
plt.figure(figsize=(10, 6))
df['price'].hist(bins=20)
plt.title('Price Distribution')
plt.xlabel('Price')
plt.ylabel('Frequency')
plt.show()
plt.close()

# Average Sales Distribution
plt.figure(figsize=(10, 6))
df['avg_sales'].hist(bins=20)
plt.title('Average Sales Distribution')
plt.xlabel('Average Sales')
plt.ylabel('Frequency')
plt.show()
plt.close()

# Boxplot for Positive Reviews
plt.figure(figsize=(10, 6))
sns.boxplot(x=df['positive_reviews'])
plt.title('Boxplot of Positive Reviews')
plt.show()
plt.close()

# Correlation Heatmap
plt.figure(figsize=(12, 8))
corr_matrix = df[['price', 'avg_sales', 'positive_reviews', 'negative_reviews']].corr()
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
plt.title('Correlation Heatmap')
plt.show()
plt.close()

# Step 6: Deeper Analysis

# Relationship between Price and Sales
plt.figure(figsize=(10, 6))
plt.scatter(df['price'], df['avg_sales'])
plt.title('Price vs. Average Sales')
plt.xlabel('Price')
plt.ylabel('Average Sales')
plt.show()
plt.close()

# Review Ratio (Positive/Negative) vs. Sales
df['review_ratio'] = df['positive_reviews'] / (df['negative_reviews'] + 1)  # Add 1 to avoid division by zero
plt.figure(figsize=(10, 6))
plt.scatter(df['review_ratio'], df['avg_sales'])
plt.title('Review Ratio (Positive/Negative) vs. Average Sales')
plt.xlabel('Review Ratio (Positive/Negative)')
plt.ylabel('Average Sales')
plt.show()
plt.close()

# Step 7: Genre Popularity for Top-Selling Games
top_10_genres = df.nlargest(10, 'avg_sales')['genres']

# Flatten the list of genres
genre_list = [genre for sublist in top_10_genres for genre in sublist]

# Count the frequency of each genre
genre_count = Counter(genre_list)
genre_df = pd.DataFrame(genre_count.items(), columns=['Genre', 'Count']).sort_values(by='Count', ascending=False)

# Display genre counts
print("\nGenre Popularity for Top-Selling Games:")
print(genre_df)

# Step 8: Impact of Publishers on Sales
top_10_publishers = df.nlargest(10, 'avg_sales')[['publishers', 'avg_sales']]
publisher_sales = {}

for index, row in top_10_publishers.iterrows():
    for publisher in row['publishers']:
        if publisher in publisher_sales:
            publisher_sales[publisher] += row['avg_sales']
        else:
            publisher_sales[publisher] = row['avg_sales']

# Convert the results into a DataFrame for better visualization
publisher_sales_df = pd.DataFrame(publisher_sales.items(), columns=['Publisher', 'Total Sales']).sort_values(by='Total Sales', ascending=False)

# Display publisher sales data
print("\nPublisher Impact on Sales:")
print(publisher_sales_df)

# Step 9: Top 10 Best-Selling Games
top_10_games = df.nlargest(10, 'avg_sales')[['name', 'price', 'avg_sales', 'positive_reviews', 'negative_reviews']]
print("\nTop 10 Best-Selling Games:")
print(top_10_games)
