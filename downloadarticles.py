import json
import csv

# Paths to your JSON files
json_files = ['art1.json', 'art2.json', 'art3.json']
combined_data = []

# Read and combine JSON data
for json_file in json_files:
    with open(json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
        combined_data.extend(data['articles'])

# Define the CSV file path
csv_file_path = 'combined_articles.csv'

# Save combined data to a CSV file
with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # Write the header
    writer.writerow(['id', 'title', 'body', 'author_id', 'created_at', 'updated_at', 'section_id', 'tags', 'content_tag_ids'])
    # Write the article data
    for article in combined_data:
        writer.writerow([
            article['id'],
            article['title'],
            article['body'],
            article['author_id'],
            article['created_at'],
            article['updated_at'],
            article['section_id'],
            ','.join(article.get('label_names', [])),  # Convert tags list to a comma-separated string
            ','.join(map(str, article.get('content_tag_ids', [])))  # Convert content_tag_ids list to a comma-separated string
        ])

print(f"Articles combined and saved successfully to {csv_file_path}")
